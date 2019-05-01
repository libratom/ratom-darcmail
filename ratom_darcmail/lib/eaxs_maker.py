#!/usr/bin/env python3

""" This module contains a class that renders EAXS XML files via Jinja2 templates. This module also
contains a private class that contains a custom Jinja2 template loader. 

Todo:
    * It would be nice to move EAXSMaker.close_folders() into a Jinja macro. I'd rather not have XML 
    specific stuff be in here. At the least, move them out into a new module ~ "eaxs_helpers.py".
"""

# import logging.
import jinja2
import logging
import os
import time
from helpers import JinjaFilters


class _TemplateLoader(jinja2.BaseLoader):
    """ A private class that contains a custom Jinja2 template loader.
    
    The loader preserves leading whitespace in each line as a way of managing XML indentation in the
    rendered files. It also removes blank lines in templates, allowing one to makes clean looking
    templates without affecting output.
    
    For more information on the jinja2.BaseLoader class, see: http://code.nabla.net/doc/jinja2/api/jinja2/loaders/jinja2.loaders.BaseLoader.html
    """


    def __init__(self, path):
        """ Sets instance attributes.
        
        Args:
            - path (str): The path to a folder that contains Jinja2 template files.
        """

        # set loggers; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.event_logger = logging.getLogger(__name__)
        self.event_logger.addHandler(logging.NullHandler())

        # set attributes.
        self.path = path


    def get_source(self, environment, template):
        """ Loads the Jinja2 @template file for a given Jinja2 @environment.
        
        Args:
            - environment (Jinja2.Environment): The template environment.
            - template (str): The path to a template file.

        Raises:
            - jinja2.TemplateNotFound: If @self.template can't be found.
        """

        # set the full path to the template file.
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            self.logger.error("Can't find template file: {}".format(path))
            raise jinja2.TemplateNotFound(path)
        
        # create container for the template data to return. 
        source = []

        # load @path; remove blank lines and preserve indentation.
        self.logger.info("Loading template file: {}".format(path))
        skipped_lines = 0

        # read through @path.
        path_file = open(path)
        for line in path_file.readlines():

            # skip blank lines.
            if line.strip() == "":
                skipped_lines += 1
                continue

            # preserve indentation.
            indent = len(line) - len(line.lstrip())
            line = (indent * " ") + line.strip()
            source.append(line)
        
        path_file.close()

        # make @source a string to return.
        self.logger.info("Loaded template has {} kept lines and removed {} blank lines.".format(
            len(source), skipped_lines))
        source = "\n".join(source)
        
        return (source, path, lambda: False)


class EAXSMaker():
    """ A class that renders EAXS XML files via Jinja2 templates. """


    def __init__(self, template_dir, charset="utf-8", *args, **kwargs):
        """ Sets instance attributes.
            
        Args:
            - template_dir (str): The path to a folder that contains Jinja2 template files.
            - charset (str): The encoding to use for writing EAXS files.
            - args/kwargs: Any optional parameters to pass to @self.make().

        Attributes:
            - ???

        Example:
            ???
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # set attributes.
        self.template_dir = template_dir
        self.charset = charset
        self.args, self.kwargs = args, kwargs
        
        # set Jinja2 environment.
        self.env = jinja2.Environment(loader=_TemplateLoader(self.template_dir), trim_blocks=True, 
            lstrip_blocks=True, comment_start_string="<!--#", comment_end_string="#-->")
        
        # create a unique string to indicate which rendered lines to omit from final output.
        # see @self.env.filters["skipnull"], below.
        self._skip_hash = "skip_" + time.time().hex()

        # add custom filters to @self.env.
        self.env.filters["skipnull"] = (lambda text: text if text is not None else self._skip_hash)
        #self.env.filters["cdata"] = (lambda text: "<![CDATA[{}]]>".format(text.strip()).replace("]]>", "]]&gt;") if
        #    text is not None else "") #TODO: Is stripping the text going to create any issues w/ quoted-printable text?
        #                              # this needs to be a standalone 
        self.env.filters.udpate(JinaFilters)


    def _write_eaxs(self, eaxs_path, template, *args, **kwargs):
        """ Handles the writing of @eaxs_path from a Jinja2 @template. This method is intended to be
        called exclusively by @self.make(). """
        
        # load @template; create a template stream to handle large output.
        eaxs_template =self.env.get_template(template)
        eaxs_stream = eaxs_template.stream(*args, **kwargs)
        
        # render the template.
        with open(eaxs_path, "w", encoding=self.charset, errors="xmlcharrefreplace") as xfile:
            
            i = 0
            for text in eaxs_stream:

                # remove any lines with @self._skip_hash in them per the "skipnull" filter.
                line = "\n".join(t for t in text.split("\n") if self._skip_hash not in t)
                xfile.write(line)
                
                # report progress as needed.
                i += 1
                if (i) % 100 == 0:
                    self.logger.info("Current write operation: {}".format(i))
        
        return


    def make(self, eaxs_path, template="Account.xml", *args, **kwargs):
        """ Creates an EAXS file at @eaxs_path by rendering the Jinja2 @template.

        Args:
            - eaxs_path (str): The filepath for the EAXS file to create.
            - template (str): The template file to render. This will be the basename of a file
            in @self.template_dir.

        Returns:
            None

        Raises:
            - FileExistsError: If @eaxs_path already exists.
            - RuntimeError: If @eaxs_path can't be rendered.
        """

        # test if @eaxs_path already exists.
        if os.path.isfile(eaxs_path):
            err = "Can't overwrite existing EAXS file: {}".format(eaxs_path)
            self.logger.error(err)
            raise FileExistsError(err)
        self.logger.info("Using template '{}' to create file: {}".format(template, eaxs_path))

        # update @args/@kwargs.
        args = args + self.args
        kwargs.update(self.kwargs)
        self.logger.debug("Template will receive args/kwargs: {}/{}".format(args, kwargs))

        # create the Jinja renderer.
        try:
            self._write_eaxs(eaxs_path, template, *args, **kwargs)
        except Exception as err:
            err = "{} | {}".format(err.__class__.__name__, err)
            self.logger.error(err)
            raise RuntimeError(err)

        return


if __name__ == "__main__":
    pass
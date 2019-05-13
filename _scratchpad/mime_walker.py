""" This module contains a class to ???

Todo
    * Normalize path seps.
"""

# import modules.
import logging
import os


class MIMEWalker():
    """ A class to ??? """


    def __init__(self, account_dir, is_eml=True):
        """ Sets instance attributes. 
        
        Args:
            - account_dir (str): ???

        Attributes:
            - ???
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # convenience functions to clean up path notation.
        self._normalize_sep = lambda p: p.replace(os.sep, os.altsep) if (
                os.altsep == "/") else p
        self._normalize_path = lambda p: self._normalize_sep(os.path.normpath(p))  

        # set attributes.
        self.account_dir = self._normalize_path(account_dir)
        self.is_eml = is_eml


    def get_files(self):
        """ ??? """

        # ???
        root = None
        for dirpath, dirnames, files in os.walk(self.account_dir):
            
            if root is None:
                root = dirpath

            for filename in files:

                filepath = os.path.join(dirpath, filename)
                print(filepath)
                self.logger.info("???".format(filepath))
                
                # ???
                if self.is_eml and not filename.lower().endswith(".eml"): 
                    self.logger.warning("???")
                    continue
                if os.path.getsize(filepath) == 0:
                    self.logger.warning("???")
                    continue
                
                # ???
                if root is None:
                    relative_filepath = os.path.relpath(root, root)
                else:
                    relative_filepath = os.path.relpath(filename, root)
                
                # ???
                results = [self._normalize_path(p) for p in [root, filename, filepath, 
                    relative_filepath]]
                
                yield results
        
        return


    def _get_eml_message(self, eml_file):
        """ ??? """

        message = None
        with open(eml_file, 'rb') as eml:
            message = email.message_from_binary_file(eml)

        return message


    def get_messages(self, mime_tuple):
        """ ??? """
        
        parse_message = lambda f: 
        if not self.eml:
            parse_mesage = email.message_from_bytes(b''.join(buff))
            
        for root, filename, filepath, relative_filepath in mime_tuple:
            




if __name__ == "__main__":
    pass

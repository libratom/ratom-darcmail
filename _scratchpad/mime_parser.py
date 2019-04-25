
 def message_generator(self, path):
        """
        This is the main method that extracts email messages from an mbox.
        :type path: str
        :param path:
        :return:
        """
        mes = None
        with open(path, 'rb') as fh:
            mes = email.message_from_binary_file(fh)
        try:
            self.logger.info("Processing Message-ID {}".format(mes.get("Message-ID")))
            self._process_message(mes, path)
            self.total_messages_processed += 1
            self.chunks += 1
        except MemoryError as me:
            # TODO: Write to a file or error log with file_id or message id
            raise MemoryError(me)
        mes = None

    def _transform_buffer(self, buff, path):
        pass

    def _process_message(self, mes, path):
        e_msg = DmMessage(self.current_relpath, CommonMethods.increment_local_id(), mes)
        e_msg.message = None
        self.messages.append(e_msg)

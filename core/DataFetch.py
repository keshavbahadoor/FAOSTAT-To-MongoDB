import config
import urllib
import zipfile
import os
import shutil
import json


class DataFetch:

    def __init__(self, log_service):
        self.log_service = log_service
        self.data_packages = json.load(open(config.DATA_PACKAGES_FILENAME))

    def import_data(self):
        # self.download_bulk_data()
        # self.extract_zipped_file(config.FAODATA_BULK_FILENAME, config.TEMP_DATA_DIR)
        self.extract_data_packages()
        # self.cleanup()

    def download_bulk_data(self):
        """
        Downloads the bulk FAOSTAT data
        :return:
        """
        try:
            self.log_service.log('Attempting to download file')
            bulkfile = urllib.URLopener()
            bulkfile.retrieve(config.BULK_FAOSTAT_DATA, config.FAODATA_BULK_FILENAME)
            return True
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            return False

    def extract_zipped_file(self, source_file, destinatin_dir):
        """
        Extracts zip file
        :return:
        """
        try:
            self.log_service.log('Unzipping {}...'.format(source_file))
            zip_ref = zipfile.ZipFile(source_file, 'r')
            zip_ref.extractall(destinatin_dir)
            zip_ref.close()
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            self.cleanup()
            return False

    def extract_data_packages(self):
        """
        Extracts each individual package as defined in json file
        :return:
        """
        try:
            for package in self.data_packages:
                file_path = os.path.join(config.TEMP_DATA_DIR, package['filename'])
                self.extract_zipped_file(source_file=file_path + '.zip', destinatin_dir=file_path)
            return True
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            self.cleanup()
            return False

    def cleanup(self):
        """
        Deletes the zip file payload that was downloaded, as well as the
        extracted data.
        :return:
        """
        try:
            self.log_service.log('Cleaning up files....')
            os.remove(config.FAODATA_BULK_FILENAME)
            shutil.rmtree(config.TEMP_DATA_DIR)
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            return False

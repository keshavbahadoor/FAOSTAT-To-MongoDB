from core.MongoService import MongoService
import config
import urllib
import zipfile
import os
import shutil
import json
import csv


class DataFetch:

    def __init__(self, log_service):
        self.log_service = log_service
        self.data_packages = json.load(open(config.DATA_PACKAGES_FILENAME))
        self.db_service = MongoService(log_service)

    def import_data(self):
        self.download_bulk_data()
        self.extract_zipped_file(config.FAODATA_BULK_FILENAME, config.TEMP_DATA_DIR)
        self.extract_data_packages()
        self.cleanup()

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
        Sends each csv file to be imported to database
        :return:
        """
        try:
            for package in self.data_packages:
                file_path = os.path.join(config.TEMP_DATA_DIR, package['filename'])
                self.extract_zipped_file(source_file=file_path + '.zip', destinatin_dir=file_path)
                for filename in os.listdir(file_path):
                    if filename.endswith('.csv'):
                        self.import_csv_file_to_database(os.path.join(file_path, filename), package['collectionname'])
            return True
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            self.cleanup()
            return False

    def import_csv_file_to_database(self, file_path, collection_name):
        """
        Imports the given file to the database
        NOTE: we delete the collection first before importing
        :param file_path:
        :return:
        """
        try:
            self.log_service.log('importing {} to database under collection {}...'.format(file_path, collection_name))
            with open(file_path, mode='r') as csvfile:
                reader = csv.DictReader(csvfile)
                self.db_service.delete_collection(collection_name)
                self.db_service.insert_data(reader, collection_name, reader.fieldnames)
        except Exception, e:
            self.log_service.log_error('Error occurred in import_csv_file_to_database', e)
            self.cleanup()
            return False

    def cleanup(self):
        """
        Deletes the zip file payload that was downloaded, as well as the
        extracted data.
        :return:
        """
        return
        try:
            self.log_service.log('Cleaning up files....')
            os.remove(config.FAODATA_BULK_FILENAME)
            shutil.rmtree(config.TEMP_DATA_DIR)
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            return False

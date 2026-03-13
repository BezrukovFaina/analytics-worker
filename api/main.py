import logging
import os
from analytics_worker import config
from analytics_worker import data_processor
from analytics_worker import data_loader

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting analytics worker')

    data_dir = config.get_data_directory()
    if not os.path.exists(data_dir):
        logging.error(f'Data directory {data_dir} does not exist')
        return

    data_files = data_loader.get_data_files(data_dir)
    if not data_files:
        logging.warning(f'No data files found in {data_dir}')
        return

    for file in data_files:
        try:
            data = data_loader.load_data(file)
            processed_data = data_processor.process_data(data)
            data_loader.save_processed_data(processed_data, file)
            logging.info(f'Successfully processed {file}')
        except Exception as e:
            logging.error(f'Error processing {file}: {str(e)}')

if __name__ == '__main__':
    main()
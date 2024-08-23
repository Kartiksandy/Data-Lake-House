import io
from datetime import timedelta
import pandas as pd
from minio import Minio
from minio.error import S3Error
from minio_config import config


def main():
    try:
        print("Connecting to Minio client...")
        client = Minio(
            'localhost:9000',
            access_key=config['access_key'],
            secret_key=config['secret_key'],
            secure=False
        )
        print("Connected to Minio client.")

        bucket_name = 'bronze'
        output_bucket_name = 'nyc-taxi-records'

        # Check if the output bucket exists, if not, create it
        if not client.bucket_exists(output_bucket_name):
            print(f"Creating bucket: {output_bucket_name}")
            client.make_bucket(output_bucket_name)
        else:
            print(f"Bucket {output_bucket_name} already exists.")

        print(f"Listing objects in bucket: {bucket_name}")
        objects = client.list_objects(bucket_name, recursive=True)

        object_found = False
        for obj in objects:
            print(f"Found object: {obj.object_name}")
            object_found = True
            if 'nyc_taxis_files' in obj.object_name:
                print(f"Processing object: {obj.object_name}")
                url = client.get_presigned_url(
                    'GET',
                    bucket_name,
                    obj.object_name,
                    expires=timedelta(hours=1)
                )

                print(f"Generated presigned URL: {url}")

                try:
                    data = pd.read_parquet(url)
                    print(f"Read parquet file: {obj.object_name}")
                    print(f"DataFrame content:\n{data}")  # Debugging step to print entire DataFrame
                except Exception as e:
                    print(f'Failed to read parquet file {obj.object_name}: {e}')
                    continue

                for index, row in data.iterrows():
                    vendor_id = str(row['VendorID'])
                    pickup_datetime = str(row['tpep_pickup_datetime'])
                    pickup_datetime_formatted = pickup_datetime.replace(':', "-").replace(' ', '_')
                    file_name = f'trip_{vendor_id}_{pickup_datetime_formatted}.json'

                    record = row.to_json()
                    print(f"Generated JSON: {record}")  # Debugging step to print JSON record
                    record_bytes = record.encode('utf-8')
                    record_stream = io.BytesIO(record_bytes)
                    record_stream_len = len(record_bytes)

                    try:
                        client.put_object(
                            output_bucket_name,
                            f'nyc_taxi_record/{file_name}',
                            record_stream,
                            length=record_stream_len,
                            content_type='application/json'
                        )
                        print(f'Uploaded {file_name} to Minio')

                        # Check if the file was created
                        found = False
                        for obj in client.list_objects(output_bucket_name, recursive=True):
                            if obj.object_name == f'nyc_taxi_record/{file_name}':
                                found = True
                                break

                        if found:
                            print(f'Successfully verified {file_name} in the bucket')
                        else:
                            print(f'Failed to verify {file_name} in the bucket')
                    except S3Error as e:
                        print(f'Failed to upload {file_name} to Minio: {e}')
                    finally:
                        record_stream.close()

        if not object_found:
            print("No objects found in the bucket.")

    except S3Error as e:
        print('Error occurred: ', e)


if __name__ == "__main__":
    main()

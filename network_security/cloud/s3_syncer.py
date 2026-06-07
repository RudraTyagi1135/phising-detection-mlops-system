import subprocess


class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        subprocess.run(
            ["aws", "s3", "sync", str(folder), str(aws_bucket_url)],
            check=True,
        )

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        subprocess.run(
            ["aws", "s3", "sync", str(aws_bucket_url), str(folder)],
            check=True,
        )

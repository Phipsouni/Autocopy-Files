import os
import sys
from shutil import copy
from time import sleep
from dotenv import load_dotenv


class FolderCopier:
    main_folder_path: str
    copy_folder_path: str
    from_what_amount_of_files_per_folder_to_copy: int

    def __init__(
        self,
        *,
        main_folder_path: str,
        copy_folder_path: str,
        from_what_amount_of_files_per_folder_to_copy: int,
    ):
        self.main_folder_path = main_folder_path
        self.copy_folder_path = copy_folder_path
        self.from_what_amount_of_files_per_folder_to_copy = (
            from_what_amount_of_files_per_folder_to_copy
        )
        self._append_folders()

    def _append_folders(self):
        sys.path.append(self.main_folder_path)
        sys.path.append(self.copy_folder_path)

    def check_main_folder(self):
        # Get the list of files and folders in the specified directory
        folder_contents = os.listdir(self.main_folder_path)

        # Filter out only the directories
        directories = [
            item
            for item in folder_contents
            if os.path.isdir(os.path.join(self.main_folder_path, item))
        ]

        for folder_in_main_folder in directories:
            content_of_the_sub_main_folder = os.listdir(
                f"{self.main_folder_path}/{folder_in_main_folder}"
            )

            if (
                len(content_of_the_sub_main_folder)
                < self.from_what_amount_of_files_per_folder_to_copy
            ):
                continue

            if folder_in_main_folder not in os.listdir(self.copy_folder_path):
                os.makedirs(f"{self.copy_folder_path}/{folder_in_main_folder}")

            content_of_the_sub_copy_folder = os.listdir(
                f"{self.copy_folder_path}/{folder_in_main_folder}"
            )

            new_files = [
                unique
                for unique in content_of_the_sub_main_folder
                if unique not in content_of_the_sub_copy_folder
            ]

            for new_file in new_files:
                copy(
                    f"{self.main_folder_path}/{folder_in_main_folder}/{new_file}",
                    f"{self.copy_folder_path}/{folder_in_main_folder}/{new_file}",
                )
                print(f"Copied {new_file}")


def main():
    load_dotenv()
    main_folder_path1 = os.getenv("main_folder_f")
    copy_folder_path1 = os.getenv("copy_folder_f1")

    f1 = FolderCopier(
        main_folder_path=main_folder_path1,
        copy_folder_path=copy_folder_path1,
        from_what_amount_of_files_per_folder_to_copy=6,
    )

    while True:
        f1.check_main_folder()
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFinished")

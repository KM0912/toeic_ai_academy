import os


class OutputDirManager:
    OUTPUT_DIR = "output"
    ACTIVE_DIR = "active"
    ARCHIVE_DIR = "archive"

    # 出力する問題文のファイル名
    QUESTION_FILE = "question.json"

    def get_active_dir_path(self):
        """
        activeディレクトリのパスを取得する

        Returns:
            str: activeディレクトリのパス
        """
        return os.path.join(self.OUTPUT_DIR, self.ACTIVE_DIR)

    def get_active_dirs(self):
        """
        activeディレクトリ内のディレクトリ名をすべて取得する

        Returns:
            list: activeディレクトリ内のディレクトリ名のリスト
        """
        active_dirs = os.listdir(os.path.join(self.OUTPUT_DIR, self.ACTIVE_DIR))
        active_dirs = sorted(active_dirs, key=int)
        return active_dirs

    def get_archive_dirs(self):
        """
        archiveディレクトリ内のディレクトリ名をすべて取得する

        Returns:
            list: archiveディレクトリ内のディレクトリ名のリスト
        """
        archive_dirs = os.listdir(os.path.join(self.OUTPUT_DIR, self.ARCHIVE_DIR))
        archive_dirs = sorted(archive_dirs, key=int)
        return archive_dirs

    def max_output_dir_number(self):
        """
        outputディレクトリ内のディレクトリ名のリストから最大の数値を取得する

        Args:
            dirs (list): ディレクトリ名のリスト

        Returns:
            int: 最大の数値
        """
        output_dirs = self.get_active_dirs() + self.get_archive_dirs()
        output_dirs = [int(d) for d in output_dirs]
        return max(output_dirs) if output_dirs else 0

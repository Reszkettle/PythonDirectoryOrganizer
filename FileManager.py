import os
import sys
import shutil
import json


class FileManager(object):

    def __init__(self, extensionsJson):
        with open(extensionsJson) as f:
            self._extensions = json.load(f)

    def reorganize(self, paths):
        for path in paths:
            self._reorganize(path)

    def _reorganize(self, path):
        filesList = [file for file in os.listdir(path) if not os.path.isdir(os.path.join(path,file))]
        filesGrouped = self._groupFilesByExtension(filesList)
        self._moveFiles(filesGrouped, path)

    def _groupFilesByExtension(self, files):
        filesGrouped = {}
        for file in files:
            group = self._getFileGroup(file)
            if group not in filesGrouped:
                filesGrouped[group] = []
            filesGrouped[group].append(file)

        return filesGrouped

    def _getFileGroup(self, file):
        for folder, extensions in self._extensions.items():
            if file.endswith(tuple(extensions)):
                return folder
        return "Other"

    def _moveFiles(self, filesGrouped, path):
        for group, files in filesGrouped.items():
            folderPath = os.path.join(path, group)
            self._createFolder(folderPath)
            self._moveFilesWithinGroup(files, path, folderPath)



    def _moveFilesWithinGroup(self, files, oldPath, newPath):

        for file in files:
            currentPath = os.path.join(oldPath, file)
            outputPath = os.path.join(newPath, file)
            if os.path.exists(outputPath):
                outputPath = self._renameFile(newPath, file)
            shutil.move(currentPath, outputPath)
        

    def _createFolder(self, path):
        if self._folderExists(path):
            return True
        try:
            os.mkdir(path)
        except OSError:
            print (f"Creation of {path} directory failed")
        else:
            return True
        return False


    def _folderExists(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            return True
        return False

    def _renameFile(self, path, filename, index=0):
        *file, ext = filename.split('.')
        newFileName = f"{'.'.join(file)}_{index}.{ext}"
        newPath = os.path.join(path, newFileName)
        if os.path.exists(newPath):
            return self._renameFile(path,filename,index+1)
        return newPath

if __name__ == '__main__':
    manager = FileManager("E:\Projects\FileManager\extensions.json")
    manager.reorganize(sys.argv[1:])


    
import os
import aiofiles
from os.path import abspath, dirname, join
import helpers.document_helper as doc_helper


async def save_file(file, name):
    filepath = join(dirname(abspath(__file__)), "tmp", name)
    async with aiofiles.open(filepath, 'wb+') as out_file:
        content = file.file.read()  # async read
        await out_file.write(content)  # async write

    print(f"file {file.filename} saved at ${filepath}")


async def delete_file(filename):
    filepath = join(dirname(abspath(__file__)), "tmp", filename)
    if os.path.isfile(filepath):
        os.remove(filepath)


def get_filelist():
    path = join(dirname(abspath(__file__)), "tmp")
    return doc_helper.get_file_list(path)

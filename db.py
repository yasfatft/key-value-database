import os, os.path

# the path we had saved our data and also dynamic data's will be save in.
data_files_path = r'/home/yasfatft/Downloads/data'
# data file must have name with same struct like what i define for example: file_number_1, file_number_2 ...
data_files_name = r'/file_number_'
# dictionary size bound(threshold)
threshold = 3


# define the main class that represent our database as key_value_db
class Key_value_db:

    # in the constructor we set the values of threshold, number of files we have on disk(file) as numOfFiles and
    # build the dictionary we used for saving our instances(key/value) in.
    def __init__(self, ):
        self.dic = {}
        self.threshold = threshold
        self.numOfFiles = len([name for name in os.listdir(data_files_path) if os.path.isfile(name)])

    # this method is implemented for copying all of instances from memory to the file when we reach the threshold and
    # then deleting them from the memory
    def copy_into_file(self):
        self.numOfFiles = self.numOfFiles + 1
        path = data_files_path + data_files_name + str(self.numOfFiles) + '.txt'
        f = open(path, "w")
        keys = list(self.dic.keys())
        keys.sort()
        for key in keys:
            instance = key + self.dic[key]
            f.write(instance)
            del self.dic[key]
        f.close()

    # according to the name of the function it do a binary search on the data that is stored into files not memory
    def binary_search(self, content, key, start, end):
        if end - start < 1:
            return None
        #
        #
        # if end - start == 1:
        #     if key == content[i * 16: i * 16 + 8]:
        #         return content[i * 16 + 8: i * 16 + 16]
        #     else:
        #         return None
        i = start + (end - start) // 2
        if key == content[i * 16: i * 16 + 8]:
            return content[i * 16 + 8: i * 16 + 16]
        elif key < content[i * 16:  i * 16 + 8]:
            return self.binary_search(content, key, start, i)
        else:
            return self.binary_search(content, key, i + 1, end)

    # set func check to see if threshold is not passed yet save data into dictionary, else it clone data into file and
    # then add key into dic
    def set(self, key, value):
        if len(self.dic) == self.threshold:
            self.copy_into_file()
        self.dic[key] = value

    # first we check the dic, if we don't find the key then we goto files ( from newest one to the oldest one because we
    # want the last value of the key ( the value may have changed during time))
    def get(self, key):
        if key in self.dic:
            return self.dic[key]
        else:
            for i in range(self.numOfFiles, 0, -1):
                path = data_files_path + data_files_name + str(i) + '.txt'
                with open(path, 'r') as content_file:
                    content = content_file.read()
                    result = self.binary_search(content, key, 0, max(self.threshold, len(content) // 16))
                    if result is None:
                        pass
                    else:
                        return result
            return None

    # save the breach block into file( it most usage is at the end of program)
    def shut_down(self):
        self.copy_into_file()


# test program
# all the keys & values must be 8 characters long
db = Key_value_db()
db.set("00000001", "0000000I")
db.set("00000002", "000000II")
db.set("00000003", "000000III")
print(db.get("00000002"))
print(db.get("00000003"))
db.set("00000001", "0000000i")  # because threshold was 3 ,at this moment the first 3 key/value save into file
db.shut_down()  # now the last key also saved into file

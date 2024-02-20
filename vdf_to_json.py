import vdf
import json
import os
import codecs

def to_raw(string):
    return fr"{string}"

def cc_txt_to_json_dump(file_location:str, Override_file_Output:str = ""):

    if file_location == "":
        print("YOU NEED TO SELECT A FILE")
        return 

    file_location = to_raw(file_location)

    vdf_file= open(file_location, "r",encoding="utf-16-le").read()

    vdf_dump = vdf.loads(vdf_file)

    json_dump = json.dumps(vdf_dump, indent=4)

    txt_filename:str = os.path.basename(file_location)

    formatd_json_filename:str = f"{txt_filename.strip('.txt')}.json"

    print(formatd_json_filename)

    final_json_path:str = f"{file_location.strip(txt_filename)}{formatd_json_filename}"

    if Override_file_Output == "":
        with open(final_json_path, "w",encoding="utf-8") as fp:
            fp.truncate()
            fp.write(json_dump)
            fp.close()
            return final_json_path
    else:
        with open(Override_file_Output, "w",encoding="utf-8") as fp:
            fp.truncate()
            fp.write(json_dump)
            fp.close()
            return Override_file_Output

def json_to_vdf_file(file_location:str ,Override_file_Output:str = ""):
    if file_location == "":
        print("YOU NEED TO SELECT A FILE")
        return 

    file_location = to_raw(file_location)

    json_file= open(file_location, "r",encoding="utf-8").read()

    json_dump:dict = json.loads(json_file)

    #Don't add escape chars to the dump since \' is actualy being read as a raw string
    #if we do escaped=True we will get a string like 'hello it\'s me' instead of 'hello it's me'
    vdf_dump:str = vdf.dumps(json_dump, pretty=True,escaped=False)

    txt_filename:str = os.path.basename(file_location)

    formatd_json_filename:str = f"{txt_filename.replace('.json','')}"

    print(formatd_json_filename)

    final_json_path:str = f"{file_location.strip(txt_filename)}{formatd_json_filename}.txt"

    if Override_file_Output == "":
        with open(file=final_json_path, mode="wb") as fp:
            fp.truncate()
            #Encode the file as UTF-16 LE BOM cause Source™ needs it to be encoded that way
            fp.write(codecs.BOM_UTF16_LE + vdf_dump.encode('utf-16-le'))
            fp.close()
            return final_json_path
    else:
        with open(file=Override_file_Output, mode="wb") as fp:
            fp.truncate()
            #Encode the file as UTF-16 LE BOM cause Source™ needs it to be encoded that way
            fp.write(codecs.BOM_UTF16_LE + vdf_dump.encode('utf-16-le'))
            fp.close()
            return Override_file_Output

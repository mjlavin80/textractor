import csv
import timing
import re
import glob
import os
import multiprocessing

try:
    cpus = multiprocessing.cpu_count()
except NotImplementedError:
    cpus = 4   # arbitrary default



RULEDICT ={}
def dict_generator(rulefile, deli='\t'):
    with open(rulefile, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=deli)
        for row in reader:
            RULEDICT[row[0]] = row[1]

def read_in_chunks(file_object, chunk_size=10240):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def multiple_replace(dict, text):
    """ Replace in 'text' all occurences of any key in the given
    dictionary by its corresponding value.  Returns the new tring."""
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

def corrector(file_folder, some_dict=RULEDICT):
    #open a file
    a= "%s/output" % file_folder[1]
    os.chdir(a)
    corrected_text = ""

    #use title to create output_version
    sourcefile_root = file_folder[0].replace(file_folder[1], '').replace('.txt', '').replace('/', '')
    output_name = sourcefile_root + "_corrected.txt"
    with open(file_folder[0]) as f:
        for piece in read_in_chunks(f):
            #replace using dict keys as guide
            corrected_lines = multiple_replace(some_dict, piece.lower())
            corrected_text += corrected_lines
            #create a tuple, using an order item, add all tuple sto list, loop list (sorted) when writing
            #write lines to new file
        with open(output_name, 'a') as o:
            o.write(corrected_text)
                    #print "Finished %s" % sourcefile_root
    os.chdir(file_folder[1])

if __name__ == "__main__":
    #loop through a director of files
    folder = raw_input("Select a folder with txt files to OCR replace: ")
    filenames = glob.glob(folder+ "/*.txt")

    dict_generator("/Users/lavin/Documents/Urules.txt")
    dict_generator("/Users/lavin/Documents/bestocr.txt")

    print "%s items added to dictionary" % len(RULEDICT.values())

    a= folder + "/output"
    if not os.path.exists(a):
        os.makedirs(a)

    filenames_tuples = [(i, folder) for i in filenames]
    #print filenames_tuples[0][1]
    pool = multiprocessing.Pool(processes=cpus)
    output = pool.map(corrector,filenames_tuples)
    #for i in filenames:

        #corrector("/Users/lavin/Dropbox/walker_text/walker_dict_1807_OCR.txt")

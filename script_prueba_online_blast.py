from Bio import Blast
from Bio import Alignment

#'''
# Blast.tool = 'biopython' # Already 'biopython' by default
Blast.email = 'bruogal@gmail.com' # They will report you via this email in case there were any problems

fasta_sequence = open('blast_practice_data/new_species.fasta').read()
result_stream = Blast.qblast("blastn", "nt", fasta_sequence) # Using Blastn to compare a nucleotide sequence against the official nucleotide (nt) database

with open('blast_query.xml', 'wb') as out_stream: # save a local XML copy of the results. First argument: document's name. Second one: type of data: wb -> write bytes
    out_stream.write(result_stream.read())
result_stream.close() # Once the results are saved, we can close the previous stream...
#'''

# PARSING results
'''
result_stream = open('blast_query.xml', 'rb') #... and reoppening it so it takes data from the saved document. rb -> read bytes
# blast_record = Blast.read(result_stream) # Blast.read() if you expect a single blast result
blast_records = Blast.parse(result_stream) # Blast.parse() if you expect lots of blast results
result_stream.close()

# Iterating through records with next()
blast_record = next(blast_records)
# ... do something with blast_record
blast_record = next(blast_records)
# ... do something with blast_record
blast_record = next(blast_records)
# ... do something with blast_record

# Using blast_records as a list. Not recommended for huge Blast files since it may cause memory problems
len(blast_records)  # this causes the parser to iterate over all records
blast_records[2].query.description # A random access to one record

# Using a for-loop
for blast_record in blast_records:
    pass  # Do something with blast_record
#'''

#'''
# Instead of opening the file yourself, you can just provide the file name:
with Blast.parse("blast_query.xml") as blast_records:
    # print (blast_records) # get a quick overview of records' contents (Bio.Blast.Records object, which is a Bio.Blast.Record iterator)
    for blast_record in blast_records:
        # Do something with blast_record (Bio.Blast.Record object, which is a list of Bio.Blast.Hit objects)
        # len(blast_record) # check how many hits does the record have
        # blast_slice_record = blast_record[:3]  # slices the first three hits. Use "blast_slice_record = blast_record[:]"" to get a full copy of the record
        # print(blast_slice_record)
        # blast_keys = blast_record.keys() # Get a list of the keys of the blast record, each key corresponding to a hit
        # blast_record["gi|262205317|ref|NR_030195.1|"] # Know wether the hit with key "gi|262205317|ref|NR_030195.1|" is present in the record or not
        # blast_record.index("gi|301171437|ref|NR_035870.1|") # if you also want to know the rank of an specific hit
        #for hit in blast_record:
            #print(hit)
        
        for alignments in blast_record: # The Bio.Blast.Hit class is a subclass of the Bio.Align.Alignments class, which contains information about the quality of the hit
            for alignment in alignments:
                if isinstance(alignment, Alignment):
                    if alignment.annotations["evalue"] < 0.04: # We show the information of those alignments whose e-value is under a certain threshold of 0.04
                        print("ALIGNMENT")
                        print("sequence: ", alignment.target.id, alignment.target.description)
                        print("length: ", len(alignment.target))
                        print("score: ", alignment.score)
                        print("e value: ", alignment.annotations["evalue"])
                        print(alignment[:, :50])
                        print()
                    else:
                        print('ALIGNMENT ABOVE THRESHOLD')
                        print("e value: ", alignment.annotations["evalue"])
                        print()
                else:
                    print('NOT AN ALIGNMENT OBJECT')
                    print()
#'''
            

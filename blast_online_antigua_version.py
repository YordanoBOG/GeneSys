from Bio.Blast import NCBIWWW, NCBIXML

'''
# Blast.tool = 'biopython' # Already 'biopython' by default
NCBIWWW.email = 'bruogal@gmail.com' # They will report you via this email in case there were any problems

fasta_sequence = open('blast_practice_data/queries/short.fasta').read()
result_handle = NCBIWWW.qblast("blastn", "nt", fasta_sequence) # Using Blastn to compare a nucleotide sequence against the official nucleotide (nt) database

with open('blast_query.xml', 'w') as out_handle: # save a local XML copy of the results. First argument: document's name
    out_handle.write(result_handle.read())
result_handle.close() # Once the results are saved, we can close the previous stream...
#'''

# PARSING results
result_handle = open('blast_query.xml') #... and reoppening it so it takes data from the saved document.
# blast_record = NCBIXML.read(result_handle) # NCBIXML.read() if you expect a single blast result
blast_records = NCBIXML.parse(result_handle) # NCBIXML.parse() if you expect lots of blast results
#result_handle.close()
'''
# Iterating through records with next()
blast_record = next(blast_records)
# ... do something with blast_record
blast_record = next(blast_records)
# ... do something with blast_record
blast_record = next(blast_records)
# ... do something with blast_record

# Using blast_records as a list. Not recommended for huge Blast files since it may cause memory problems
blast_records = list(blast_records)

# Using a for-loop
for blast_record in blast_records:
    pass  # Do something with blast_record
#'''

#'''
# print (blast_records) # get a quick overview of records' contents (Bio.Blast.Records object, which is a Bio.Blast.Record iterator)
for blast_record in blast_records:
    # len(blast_record) # check how many hits does the record have
    # blast_slice_record = blast_record[:3]  # slices the first three hits. Use "blast_slice_record = blast_record[:]"" to get a full copy of the record
    # print(blast_slice_record)
    # blast_keys = blast_record.keys() # Get a list of the keys of the blast record, each key corresponding to a hit
    # blast_record["gi|262205317|ref|NR_030195.1|"] # Know wether the hit with key "gi|262205317|ref|NR_030195.1|" is present in the record or not
    # blast_record.index("gi|301171437|ref|NR_035870.1|") # if you also want to know the rank of an specific hit
    print ("BLAST RECORD")
    for alignment in blast_record.alignments: # The Bio.Blast.Hit class is a subclass of the Bio.Align.Alignments class, which contains information about the quality of the hit
        print("ALIGNMENT")
        for hsp in alignment.hsps:
            if hsp.expect < 0.04:
                print("****Alignment****")
                print("sequence:", alignment.title)
                print("length:", alignment.length)
                print("e value:", hsp.expect)
                print(hsp.query[0:75] + "...")
                print(hsp.match[0:75] + "...")
                print(hsp.sbjct[0:75] + "...")
                print()
            else:
                print("****Alignment UNDER TRESHOLD****")
                print("e value:", hsp.expect)
                print()
#'''
            

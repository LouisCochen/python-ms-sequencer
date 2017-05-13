# python-ms-sequencer
Tiny Python script for de novo sequencing from a list of peaks of a MS/MS spectrum

I wrote the first version of this for my Mass Spec module, it had a lot of flaws so I decided to make a new one and share it.

Here it is, my new MS de novo sequencer for peptides cut using trypsin !

It is still version 0.0.1, far from finished but works in most occasions (high success rate up to 200 residues).

It reads from an input of peaks obtained in the MS/MS experiment.

The sequencing works as follows :
>  1 - initiation :  
- finding K or R as the C-term amino acid
- starting wirting the sequence
- add the m/z list of both y" and b ion of R/K
                  
>  2 - sequencing :  
- using the m/z of y"(n) and b(n) ion + m/z of residues (stored in the dictionnaries), look for the possible amino acids going C to N termini.
- if only one if found, add to sequence, add the m/z to list for y" and b ion

>  3 - termination : 
- when m/z(y" ions) = m/z of molecular ions or m/z(b ions) = 1 stop sequencing
- create values for m/z of the ions found
- search for a ions
- output + timer

This version will work for most of the easy sequencing.

You can test with the random generator to create the peaks of random sequences and use as input for troubleshooting.

The things I'll implement soon are :
- re-read using the second possible peak if several are found
- better output
- maybe read/write .txt files for input output if desired
- OCR so that it takes a .pdf file as input, will need verification by user

Some of the variable present in the current version are not used but they'll be useful when I implement more things.

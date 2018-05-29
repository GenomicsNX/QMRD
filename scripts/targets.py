


# targets and information
###################################3


# ####################################
# criteria for finding targets
# #####################################
# pos_in : position regular expression that should be matched, pos_out that should not matched
# cigar_in : cigar string regular expression that should be matched, cigar_out that should not matched
# seq_in : sequence string regular expression that should be matched, seq_out that should not matched
# ##########################################


# expression
ABL1=dict(ref='chr9',start=130714369,end=130854114,cigar_in="M1396[0-1][1-9]N",catg='expr')
WT1=dict(ref='chr11',start=32428042,end=32434722,cigar_in="M438N",catg='expr')
PRAME=dict(ref='chr22',start=22548424,end=22548559,catg='expr')
PRAME_str=dict(ref='chr22',start=22548424,end=22548559,seq="^CGT",cigar_in="13[0-9]M$",catg='expr')
NPM1=dict(ref='chr5',start=171407744,end=171410635,pos=1714077,cigar_in="[0-9]M2752N[0-9][0-9][0-9]M",cigar_out="4I",catg='expr')
NPM1_mutant=dict(ref='chr5',start=171407744,end=171410635,cigar_in="[0-9]M2752N[0-9][0-9]M4I",catg='expr')


CBFB_MYH1=dict(r1=dict(ref='chr16',start=67066750,end=67082308,cigar_in="[7-8][0-9]M[4-5][0-9]S"),
				   r2=dict(ref='chr16',start=15720994,end=15721051,cigar_in="[4-5][0-9]M[7-8][0-9]S"),catg='fusion')

RUNX1_RUNX1T1=dict(r1=dict(ref='chr21',start=34859474,end=34859556,cigar_in="[5-6][0-9]S[6-7][0-9]M"),
				   r2=dict(ref='chr8',start=92017298,end=92017363,cigar_in="[5-6][0-9]M[6-7][0-9]S"),catg='fusion')

PML_RARA_bcr1=dict(r1=dict(ref='chr15',start=74033319,end=74033414,cigar_in="[4-5][0-9]M[8-9][0-9]S"),
				   r2=dict(ref='chr17',start=40348316,end=40348396,cigar_in="[4-5][0-9]S[8-9][0-9]M"),catg='fusion')


PML_RARA_bcr3=dict(r1=dict(ref='chr15',start=74023343,end=74023408,cigar_in="[8-9][0-9]M[4-5][0-9]S"),
				   r2=dict(ref='chr17',start=40348316,end=40348396,cigar_in="[8-9][0-9]S[4-5][0-9]M"),catg='fusion')
				   

BCR_ABL1_p190=dict(r1=dict(ref='chr22',start=23182069,end=23182239,cigar_in="[8-9][0-9]M[4-5][0-9]S"),
				   r2=dict(ref='chr9',start=130854064,end=130854114,cigar_in="[8-9][0-9]S[4-5][0-9]M"),catg='fusion')


BCR_ABL1_b3a2=dict(r1=dict(ref='chr22',start=23289558,end=23290413,cigar_in="[6-7][0-9]M[4-5][0-9]S"),
				   r2=dict(ref='chr9',start=130854064,end=130854114,cigar_in="[8-9][0-9]S[4-5][0-9]M"),catg='fusion')

BCR_ABL1_b2a2=dict(r1=dict(ref='chr22',start=23289558,end=23289621,cigar_in="[8-9][0-9]M[4-5][0-9]S"),
				   r2=dict(ref='chr9',start=130854064,end=130854114,cigar_in="[8-9][0-9]S[4-5][0-9]M"),catg='fusion')


	
dct_of_targets={'ABL1':ABL1,'WT1':WT1,'PRAME':PRAME_str,'NPM1':NPM1,'NPM1_mutant':NPM1_mutant,
				'CBFB_MYH1':CBFB_MYH1,'RUNX1_RUNX1T1':RUNX1_RUNX1T1,'PML_RARA_bcr1':PML_RARA_bcr1,
				'PML_RARA_bcr3':PML_RARA_bcr3,'BCR_ABL1_p190':BCR_ABL1_p190,'BCR_ABL1_b3a2':BCR_ABL1_b3a2,
				'BCR_ABL1_b2a2':BCR_ABL1_b2a2}

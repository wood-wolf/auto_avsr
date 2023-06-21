nbpe=5000
bpemode=unigram
mkdir -p ${bpemode}
dict=${bpemode}/${bpemode}${nbpe}_units.txt
bpemodel=${bpemode}/${bpemode}${nbpe}
bpemode_zh=unigram_zh  # xx
mkdir -p ${bpemode_zh}  # xx
dict_zh=${bpemode_zh}/${bpemode}${nbpe}_units.txt  # xx
bpemodel_zh=${bpemode_zh}/${bpemode}${nbpe}  # xx
echo "<unk> 1" > ${dict_zh} # <unk> must be 1, 0 will be used for "blank" in CTC
python spm_train.py --input=input_zh.txt --vocab_size=${nbpe} --model_type=${bpemode} --model_prefix=${bpemodel_zh} --input_sentence_size=100000000  # xx
python spm_encode.py --model=${bpemodel_zh}.model --output_format=piece < input_zh.txt | tr ' ' '\n' | sort | uniq | awk '{print $0 " " NR+1}' >> ${dict_zh}  # xx

BASEDIR=$(dirname $0)

rm -rf docbook
python $BASEDIR/im.py $BASEDIR/FileTranslations . docbook/

echo '=================================================='

cd docbook
find . -type f -print0 | xargs -0 sed -i 's/<br>/\n/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br>/\n/g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/>/\n/g'
find . -type f -print0 | xargs -0 sed -i 's/<ul>//g'
find . -type f -print0 | xargs -0 sed -i 's/<\/ul>//g'
find . -type f -print0 | xargs -0 sed -i 's/<ul\/>//g'
find . -type f -print0 | xargs -0 sed -i 's/<li>//g'
find . -type f -print0 | xargs -0 sed -i 's/<\/li>//g'
find . -type f -print0 | xargs -0 sed -i 's/<li\/>//g'
find . -type f -print0 | xargs -0 sed -i 's/..\/images\//images\//'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/\(!\[.*\](.*)\)[\n[ ]*]*\n[ ]*\*\*.*\*\*/\1/;P;D'
python $BASEDIR/con.py ./SUMMARY.md docbook
cd docbook
find . -type f -print0 | xargs -0 sed -i 's/sect1/section/g'
find . -type f -print0 | xargs -0 sed -i 's/sect2/section/g'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/<para>\n[ ]*<emphasis role="strong">介绍<\/emphasis>\n[ ]*<\/para>/<formalpara><title>介绍<\/title><para><\/para><\/formalpara>/;P;D'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/<para>\n[ ]*<emphasis role="strong">概述<\/emphasis>\n[ ]*<\/para>/<formalpara><title>概述<\/title><para><\/para><\/formalpara>/;P;D'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/<para>\n[ ]*<emphasis role="strong">结果<\/emphasis>\n[ ]*<\/para>/<formalpara><title>结果<\/title><para><\/para><\/formalpara>/;P;D'
find . -type f -execdir python $BASEDIR/xmlmod.py {} \;
find . -type f -print0 | xargs -0 sed -i 's/\(<imagedata fileref="\)\(.*png" \)\(\/>\)/\1\2format="PNG" scale="50" \3/'

cp -r ../../images/ ./zh-CN

publican build --formats=pdf --langs=zh-CN --brand_dir=/usr/share/publican/Common_Content/eayun

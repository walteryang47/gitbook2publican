BASEDIR=$(dirname $0)

rm -rf docbook
python $BASEDIR/im.py $BASEDIR/FileTranslations . docbook/

echo '=================================================='

cd docbook
python $BASEDIR/con.py ./SUMMARY.md docbook
cd docbook
find . -type f -print0 | xargs -0 sed -i 's/sect1/section/g'
find . -type f -print0 | xargs -0 sed -i 's/sect2/section/g'
find . -type f -print0 | xargs -0 sed -i 's/<br>//g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br>//g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/>//g'
publican build --formats=pdf --langs=zh-CN --brand_dir=.

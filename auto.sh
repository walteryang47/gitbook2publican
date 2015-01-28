rm -rf docbook
python ~/projects/ey/gb2db/im.py ~/projects/ey/gb2db/FileTranslations . docbook/

echo '=================================================='

cd docbook
python ~/projects/ey/gb2db/con.py ./SUMMARY.md docbook
cd docbook
find . -type f -print0 | xargs -0 sed -i 's/sect1/section/g'
find . -type f -print0 | xargs -0 sed -i 's/sect2/section/g'
find . -type f -print0 | xargs -0 sed -i 's/<br>//g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br>//g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/>//g'
publican build --formats=pdf --langs=zh-CN --brand_dir=.

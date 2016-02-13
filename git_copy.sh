#!/bin/sh
if [[ "$#" -lt "1" || "$#" -gt "2" ]]; then
    echo -e "Usage:\n"\
          "\t$0 <source file path> [destination file path]\n\n"\
          "\tsource and destination paths should within git repositories\n"\
          "\twithout dest file path given the file will be created into the current directory"
    exit -1
fi
#set -x
src_abs=$(readlink -e $1)
dst_root=$(git rev-parse --show-toplevel)
dst=${2-$(basename $src_abs)}
dst_abs=$(readlink -f $dst)  # the destination path should be existent except the file
if [ -z "$dst_abs" ]; then echo mkdir -p $(dirname $dst); exit; fi
dst_rel=$(echo $dst_abs | sed "s#$dst_root/##g")
pushd $(dirname $src_abs) > /dev/null
src_root=$(git rev-parse --show-toplevel)
src_rel=$(echo $src_abs | sed "s#$src_root/##g")
outfile=$(basename $dst_rel)_$(date +%s).patch
git format-patch --stdout \
$(git log $(basename $src_abs) | grep ^commit|tail -1|awk '{print $2}')^..HEAD $(basename $src_abs) |\
sed "s#$src_rel#$dst_rel#g" |\
awk 'BEGIN{ena=1} /^diff /{ if ( $0 ~ /'$(echo "$dst_rel" | sed 's#/#\\/#g')'$/ ) ena=1; else ena=0 } { if (ena==1) print; }' |\
(popd > /dev/null; cat > $outfile)
echo $src_root///$src_rel " -->  $dst_root///$dst_rel"
echo git am $outfile




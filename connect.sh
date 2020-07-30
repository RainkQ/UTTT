echo "player type: $1, lobby: $2"
if [ $1 == 0 ]
then
    uabc --host "http://10.127.246.165:3141" --lobby "$2" --token "random" -f "python run_player.py -t $1"
elif [ $1 == 1 ]
then
    uabc --host "http://10.127.246.165:3141" --lobby "$2" --log --token "mstc-v0" -f "python run_player.py -t $1"
fi
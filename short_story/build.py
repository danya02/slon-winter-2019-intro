#!/usr/bin/python3
import random
import jinja2
import os
print(f'Running in {os.getcwd()}...')
if 'short_story' not in os.getcwd():
    print('Going into dir short_story to work.')
    os.chdir('short_story')
d = open('main.md').read()
mc='James'
sc='Simon'
scscreen='yamadasam'
bm='Tom'
mk='Monika'


# from source code for DDLC
def glitchtext(length):
    nonunicode = "¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž"
    output = ""
    for x in range(length):
        output += random.choice(nonunicode)
    return output

def z(text,frequency,intensity):
    # Zalgificator adapted from https://github.com/cosmicexplorer/zalgify
    diacritics= ['̍', '̎', '̄', '̅', '̿', '̑', '̆', '̐', '͒', '͗', '͑', '̇', '̈', '̊', '͂', '̓', '̈', '͊', '͋', '͌', '̃', '̂', '̌', '͐', '̀', '́', '̋', '̏', '̒', '̓', '̔', '̽', '̉', 'ͣ', 'ͤ', 'ͥ', 'ͦ', 'ͧ', 'ͨ', 'ͩ', 'ͪ', 'ͫ', 'ͬ', 'ͭ', 'ͮ', 'ͯ', '̾', '͛', '͆', '̚','̖', '̗', '̘', '̙', '̜', '̝', '̞', '̟', '̠', '̤', '̥', '̦', '̩', '̪', '̫', '̬', '̭', '̮', '̯', '̰', '̱', '̲', '̳', '̹', '̺', '̻', '̼', 'ͅ', '͇', '͈', '͉', '͍', '͎', '͓', '͔', '͕', '͖', '͙', '͚', '̣','̕', '̛', '̀', '́', '͘', '̡','̢', '̧', '̨', '̴', '̵', '̶', '͜', '͝', '͞', '͟', '͠', '͢', '̸', '̷', '͡', ' ҉']
    text=list(text)
    for i,j in enumerate(text):
        if random.random()>(float(frequency)/10):
            pass
        else:
            zalgified=j
            for n in range(intensity):
                zalgified+=random.choice(diacritics)
            text[i]=zalgified
    return ''.join(text)

j=jinja2.Template(d)
d=j.render(**locals())
with open('outp.md','w') as o:
    o.write(d)

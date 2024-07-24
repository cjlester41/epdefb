def next_alpha(airport_chr):    # generate next character in unicode sequence

    if ord(airport_chr) == 57:
        airport_chr = '@'
    airport_chr = chr((ord(airport_chr)+1 - 48) % 43 + 48)
    #show_chr(airport_chr, cursor=True)
    return airport_chr
        
def prev_alpha(airport_chr):    # generate previous character in unicode sequence

    if ord(airport_chr) == 65:
        airport_chr = ':'
    airport_chr = chr((ord(airport_chr)-1 - 48) % 43 + 48)
    #show_chr(airport_chr, cursor=True)
    return airport_chr

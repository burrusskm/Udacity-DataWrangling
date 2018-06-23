for value in postalcodes:
    value = value.replace('-', '')
    m = postalcode_re.search(value)
    if m:
        return(value)
    else:
        problematics.append(value)
    # am I to be adding to the problematics list here?

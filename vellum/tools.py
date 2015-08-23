from bs4 import NavigableString, BeautifulSoup
import click
import codecs
import os
import re


def clip_text(soup):
    """Modify a BeautifulSoup instance in-place to strip all its text back to
    the first few words. Use this to show useful structure without violating
    copyright.

    Example usage:
In [70]: from bs4 import BeautifulSoup; import tools

In [80]: soup = BeautifulSoup(open('vellum.html'), 'html.parser')

In [81]: tools.clip_text(soup)

In [82]: f = codecs.open('clipped.html', 'w', encoding='utf-8')

In [83]: f.write(soup.prettify())

In [84]: f.close()
    """
    if soup.name in ('h1', 'h2', 'h3', 'h4', 'h5'):
        pass  # Preserve heading structure!
    elif isinstance(soup, NavigableString):
        index = max(10, soup.find(' ', 10))
        if len(soup) > index:
            soup.replace_with(soup[:index] + u'\u2026')  # unicode ellipsis
    else:
        map(clip_text, soup.contents)


def str_iter(soup):
    if isinstance(soup, NavigableString):
        yield soup
    else:
        if 'annotation' in soup.get('class', []):
            return
        for content in soup.contents:
            for s in str_iter(content):
                yield s


note_counter = 1


def site_annotations(soup, top_level_soup):
    global note_counter

    annotations = []
    for content in list(soup.contents):
        if isinstance(content, NavigableString):
            pass
        elif 'annotation' in content.get('class', []):
            annotations.append(content.extract())
        else:
            site_annotations(content, top_level_soup)
    contents = list(soup.contents)
    for annotation in annotations:
        new_contents = []
        found = False
        for content in contents:
            if found:
                new_contents.append(content)
            else:
                if isinstance(content, NavigableString):
                    split_content = content.split(annotation['data-anchor'])
                    if len(split_content) > 1:
                        found = True
                        new_label = top_level_soup.new_tag('label')
                        new_label['class'] = 'margin-toggle annotation-anchor'
                        new_label['for'] = 'note{}'.format(note_counter)
                        new_label.string = annotation['data-anchor']
                        new_input = top_level_soup.new_tag('input')
                        new_input['type'] = 'checkbox'
                        new_input['id'] = 'note{}'.format(note_counter)
                        new_input['class'] = 'margin-toggle'
                        annotation['data-anchor'] = None
                        annotation['class'].append('marginnote')
                        new_contents.extend((
                            NavigableString(split_content[0]),
                            annotation,
                            new_label,
                            new_input,
                            NavigableString(split_content[1])))
                        note_counter += 1
                    else:
                        new_contents.append(content)
        if found:
            soup.contents = new_contents
        else:
            raise ValueError('Annotation ' + annotation + ' not found')


def reinflate(template, source):
    template = BeautifulSoup(template, 'html.parser')
    source = BeautifulSoup(source, 'html.parser')

    template_strings = str_iter(template.body)
    source_strings = str_iter(source.body)

    s = t = ''
    try:
        while True:
            while not t.strip():
                t = template_strings.next()
            while not s.strip() or s.strip() == '*':
                s = source_strings.next()
            if unicode(s).strip().lower().startswith(unicode(t)[:10].strip().lower()):
                # print u'{} -> {}\n'.format(t[:10], s)
                t.replace_with(unicode(s))
            else:
                raise ValueError(u"Missing something!\n[{}]\n[{}]".format(t[:10], s))
            s = t = ''
    except StopIteration:
        pass
    return template


def reinflate_file(template_fname, source_fname, out_fname):
    template = open(template_fname)
    source = open(source_fname)
    inflated = reinflate(template, source)
    template.close()
    source.close()
    out = codecs.open(out_fname, 'w', 'utf8')
    out.write(unicode(inflated))
    out.close()
    out = codecs.open(out_fname, 'r', 'utf8')
    f_as_str = out.read()
    f_as_str = f_as_str\
        .replace(
        'Pechorin (bioform) status: personality by-pass operation complete.',
        ('</p>\n<p class="mechanical"><strong>Pechorin (bioform) status:</stro'
         'ng> personality by-pass operation complete.</p>'))\
        .replace(
        'I am legion; the kingdom is within us.',
        'I am legion; <span class="mundane">the kingdom is within us.</span>')
    f_as_str = re.sub(r'</em>[ \n]+<em>', ' ', f_as_str)

    soup = BeautifulSoup(f_as_str, 'html.parser')
    site_annotations(soup, soup)

    out = codecs.open(out_fname, 'w', 'utf8')
    out.write(unicode(soup))
    out.close()


@click.command()
@click.argument('ebook', type=click.Path(exists=True))
@click.argument('out', type=click.Path(exists=False))
def expand_vellum(ebook, out):
    clipped_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'clipped.html')
    reinflate_file(clipped_filename, ebook, out)

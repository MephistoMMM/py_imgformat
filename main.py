#!/usr/local/Cellar/python3/
"""
a tool to change the format of picture to png(default);

@author MephistoPheies
@createDate 2015/8/7
@upDate     2015/8/7
"""


import os
from PIL import Image
import optparse
import funForCorutine as ffc

class inputError(Exception) : pass

VALIDTYPE = ['png','jpg','jpge','tiff']
DEFAULTRESULTTYPE = 'png'
DEFAULTAIMTYPE = 'tiff'
RESULTINDEX = 'mpifc_result'
PROTONAME = False

resultType = 'png'
protoName = False
aimType = 'tiff'
result = {'error': 0,'num':0, 'reason':[]}

def main():
    indexPaths, opts = argvsReady()

    global resultType, aimType, protoName
    resultType = opts.rType
    aimType = opts.aType
    protoName = opts.pName

    starter, closer = coroutineCreator()

    for indexPath in indexPaths:
        starter.send(indexPath)

    closer()
    outPut()



def outPut():
    """
    """
    outStr = '\nChanged picture: {}\nErrors: {}\n'.format(
                result['num'],result['error'])

    for re in result['reason']:
        outStr = outStr + '{: ^8}{}\n'.format('',re)

    print(outStr)



def errors(string):

    global result
    result['error'] += 1
    result['reason'].append(string)


def coroutineCreator():
    """
    construct the assembly line
    """
    fWriter = imageWriter(None)
    fLoader = imageLoader(fWriter)
    fFilter = fileFilter(fLoader) 
    fWalker = dirWalker(fFilter)
    starter = fWalker

    return ffc.cteContrlCreator(
            fWriter,
            fLoader,
            fFilter,
            starter = fWalker)



def argvsReady():
    """pack up argvs"""
    parser = optparse.OptionParser('Usage: python3 fileToPng '
            'Path[,Path2,Path3...] [Option]')
    parser.add_option('-r', '--rtype', dest='rType',
            help = ('defined the format of result'
                    '[default:%default]'))
    parser.add_option('-a', '--atype', dest='aType',
            help = ('defined the format of aim'
                    '[default:%default]'))
    parser.add_option('-p', '--protoname', action='store_true', dest='pName',
            help = ('use proto name to name resultFile'
                    '[default:%default]'))

    parser.set_defaults(rType = DEFAULTRESULTTYPE, 
                        aType = DEFAULTAIMTYPE,
                        pName = PROTONAME)

    opts, argvs = parser.parse_args()
    opts.rType = opts.rType if opts.rType in VALIDTYPE else DEFAULTRESULTTYPE
    opts.aType = opts.aType if opts.aType in VALIDTYPE else DEFAULTAIMTYPE
    
    if opts.rType == opts.aType :
        raise inputError('Wrong at option: rType == aType.') 
    if len(argvs) == 0:
        raise inputError('Wrong at option: lack Path argument')

    return argvs, opts



@ffc.coroutine
def dirWalker(reciever):
    """
    walk dirs and get files
    """

    while True: 
        indexPath = (yield)

        try: 
            for root, dirs, files in os.walk(indexPath):
                os.mkdir(os.path.join(root, RESULTINDEX))
                reciever.send((files, dirs,root))
        
        except Exception as err:
            errors('Failed to walk dirs at {}, details:{}'.format(
                        root,err))


@ffc.coroutine
def fileFilter(reciever):
    """
    filter the aimType file
    """
    def isValidFiles(file):
        """
        filter file to get the valid files
        """

        pointPosition = file.find('.')

        if(pointPosition == 0 or pointPosition == -1):
            return False

        elif(not file.rsplit('.',1)[1] in aimType):
            return False

        else:
            return True

    def isValidDirs(dir):
        """
        this dirs cloudn't be start with '.'
        """
        return False if dir[0] == '.' else True;


    while True:
        files, dirs, root = (yield)

        try: 
            files = list(filter(isValidFiles, files))
            dirs[:] = list(filter(isValidDirs, dirs))

            if len(files) > 0:
                reciever.send((files, root))

        except Exception as err:
            errors('Failed to filter files at {}, details:{}'.format(
                        root,err))


@ffc.coroutine
def imageLoader(reciever):
    """
    change image format
    """
    def changeName(file):
        """
        get the new FileName
        """
        nonlocal count
        
        if protoName :
            count = os.path.splitext(file)[0]
        else:
            count += 1

        name = '{}/{}.{}'.format(RESULTINDEX, count, resultType)

        return os.path.join(root, name)


    while True:
        files, root = (yield)

        try:
            count = 0;
            newFiles = list(map(changeName, files))
            oldFiles = list(map(lambda x: os.path.join(root, x),
                                    files))

            for oldFile, newFile in zip(oldFiles, newFiles):
                reciever.send((
                    newFile, oldFile, Image.open(oldFile)))


        except Exception as err:
            errors('Failed to load image at {}, details:{}'.format(
                        root, err))


@ffc.coroutine
def imageWriter(reciever):
    """
    write the image
    """

    while True:
        newFile, oldFile, im = (yield)

        try:
            global result
            im.save(newFile)
            result['num'] += 1
            print('{} --{}---{}--> over'.format(
                oldFile, aimType, resultType))
        
        except Exception as err:
            errors('Failed to write image {}, details:{}'.format(
                        oldFile, err))
            


try:
    main()

except inputError as err:
    print(err)
#except Exception as err:
    print('program err:')
    print(err)


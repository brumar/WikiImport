import logging, json, importio, latch
import anki
import PyQt4.QtNetwork
import aqt
import useroptions
from aqt.utils import showInfo
from PyQt4 import QtGui
from importer import *


wiki_MODEL="wiki_note"
TITLE_FIELD_NAME="title"
CONTENT_FIELD_NAME="content"


class Anki:
    def addwikiCards(self, wikiCards,deck,tags):
        count=0
        modelName=wiki_MODEL
        for card in wikiCards:
            ankiFieldInfo = {}
            ankiFieldInfo[TITLE_FIELD_NAME] = card.front.decode('utf-8')
            ankiFieldInfo[CONTENT_FIELD_NAME] = card.back.decode('utf-8')
            noteId = self.addNote(deck, modelName,ankiFieldInfo,tags)
            count+=1
        self.stopEditing()
        return count

    def addNote(self, deckName, modelName, fields, tags=list()):
        note = self.createNote(deckName, modelName, fields, tags)
        if note is not None:
            collection = self.collection()
            collection.addNote(note)
            collection.autosave()
            self.startEditing()
            return note.id

    def createNote(self, deckName, modelName, fields, tags=list()):
        idDeck=self.decks().id(deckName)
        model=self.models().byName(modelName)
        col=self.collection()
        note = anki.notes.Note(col,model)
        note.model()['did'] = idDeck
        note.tags = tags
        for name, value in fields.items():
            note[name] = value
        return note

    def add_wiki_model(self): #adapted from the IREAD plug-in from Frank
        col = self.collection()
        mm = col.models
        wiki_model = mm.byName(wiki_MODEL)
        if wiki_model is None:
            wiki_model = mm.new(wiki_MODEL)
            # Field for title:
            model_field = mm.newField(TITLE_FIELD_NAME)
            mm.addField(wiki_model, model_field)
            # Field for text:
            text_field = mm.newField(CONTENT_FIELD_NAME)
            mm.addField(wiki_model, text_field)
            # Add template
            t = mm.newTemplate('wikiReview')
            t['qfmt'] = "{{"+TITLE_FIELD_NAME+"}}"
            t['afmt'] = "{{"+CONTENT_FIELD_NAME+"}}"
            mm.addTemplate(wiki_model, t)
            mm.add(wiki_model)
            return wiki_model
        else:
            fmap = mm.fieldMap(wiki_model)
            title_ord, title_field = fmap[TITLE_FIELD_NAME]
            text_ord, text_field = fmap[CONTENT_FIELD_NAME]

    def getGuidsFromAnkiId(self,ids):
        guids=[]
        for a_id in ids:
            card = self.collection().getCard(a_id)
            items=card.note().items()
            if(len(items)==3):
                guids.append(items[2][1])#not a very smart access
        return guids

    def canAddNote(self, deckName, modelName, fields):
        return bool(self.createNote(deckName, modelName, fields))




    def getCardsIdFromTag(self,tag):
        query="tag:"+tag
        ids = self.collection().findCards(query)
        return ids

    def browseNote(self, noteId):
        browser = aqt.dialogs.open('Browser', self.window())
        browser.form.searchEdit.lineEdit().setText('nid:{0}'.format(noteId))
        browser.onSearch()


    def startEditing(self):
        self.window().requireReset()


    def stopEditing(self):
        if self.collection():
            self.window().maybeReset()


    def window(self):
        return aqt.mw


    def addUiAction(self, action):
        self.window().form.menuTools.addAction(action)


    def collection(self):
        return self.window().col

    def manager(self):
        return self.decks().DeckManager(self.window())


    def models(self):
        return self.collection().models


    def modelNames(self):
        return self.models().allNames()


    def modelFieldNames(self, modelName):
        model = self.models().byName(modelName)
        if model is not None:
            return [field['name'] for field in model['flds']]


    def decks(self):
        return self.collection().decks


    def deckNames(self):
        return self.decks().allNames()


    def curModelID(self):
        return self.collection().conf['curModel']


    def curDeckID(self):
        return self.collection().conf['curDeck']


    def curModel(self):
        return self.models().get(self.curModelID())


    def curDeck(self):
        return self.decks().get(self.curDeckID())


    def curModelName(self):
        return self.curModel()['name']


    def curDeckName(self):
        return self.curDeck()['name']


class getInfo(QtGui.QWidget):

    def __init__(self,input):
        self.input=input
        super(getInfo, self).__init__()

        #self.initUI()

    def initUI(self):

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def showDialog(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',self.input)

        if ok:
            return(str(text))
        return None

def main():
    anki = Anki()
    anki.add_wiki_model()
    if(useroptions.api_key=="" or useroptions.user_id==""):
        showInfo("your import.io account informations has not been given, please follow the instructions provided at the plug-in page")
        return
    categ=getInfo('Enter a link to a wikipedia category (e.g http://en.wikipedia.org/wiki/Category:Learning_methods) ')
    categUrl=categ.showDialog()
    if(categUrl):
        deck = getInfo('Enter the name of the deck you want to create (e.g learningMethods)')
        deckName=deck.showDialog()
    if(categUrl and deckName):
        showInfo("import.io is working for you, please wait a few minutes")
        cards=GenerateAnkiCardsFromWikipediaCategory(categUrl,deckName,useroptions.user_id,useroptions.api_key)
        number=anki.addwikiCards(cards,deckName,tags=["wiki"])
        text=deckName+"have been created with "+str(number)+" cards"
        aqt.utils.tooltip(text, 3000)


    #controller.addNoteToDeck(c)

action = aqt.qt.QAction("wikipedia import", aqt.mw)
aqt.mw.connect(action,  aqt.qt.SIGNAL("triggered()"), main)
aqt.mw.form.menuTools.addAction(action)
import tornado.ioloop
import tornado.web
import os.path
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.gen
import motor
import json
from bson import BSON
from bson import json_util

import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from foundling_globals import aws_public_key, aws_secret_key, mongo_db, foundling_aws_base_url

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
        def __init__(self):
                handlers =      [

                                (r"/", IndexHandler),
				(r"/sounds", SoundsHandler),
                                (r"/uploadwav", UploadWAVHandler),
				(r"/map", MapHandler)
                                ]

                settings = dict(
                                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                static_path=os.path.join(os.path.dirname(__file__), "static"),
                                debug = True
                                )

                tornado.web.Application.__init__(self, handlers, **settings)

		
		client = motor.MotorClient(mongo_db)
		self.db = client['foundsound']

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")

class UploadWAVHandler(tornado.web.RequestHandler):
	#this class post action receives a wav file and uploads the file to amazon s3
	
	def mycb(so_far, total):
		print '%d bytes transferred out of %d' % (so_far, total)

	def get(self):
		self.render('wavupload.html')

	def post(self):
		wav = self.request.files['wav'][0] #wav post data from form
		wavbody = wav['body'] #body of wav file
		wavname = wav['filename'] #wav name and path
		
		conn = S3Connection(aws_public_key, aws_secret_key)
		bucket = conn.get_bucket('foundsound_wav') #bucket for wavs

		k = Key(bucket) #key associated with wav bucket
		k.key = wavname #sets key to image name
		k.set_metadata("Content-Type", "audio/wav") #sets metadata for audio/wav
		k.set_contents_from_string(wavbody)#, cb=self.mycb(), num_cb=1000)
		#k.set_contents_from_file(wav)
		k.set_acl('public-read') #makes wav public

		self.write("uploaded!")

class SoundsHandler(tornado.web.RequestHandler):
#this handler returns all sounds in sounds collection
	@tornado.web.asynchronous
	@tornado.gen.coroutine	
	def get(self):
		sounds = {} #set up a dictionary to hold json
		all_sounds = [] #set up a list to hold sounds from mongodb
		cursor = self.application.db.sounds.find({}) #set up a cursor with all objects in sounds collection
		while (yield cursor.fetch_next): #yield a future to get the result
			sound = cursor.next_object() #get sound as next object
			all_sounds.append(sound) #add sound to all sounds list
		sounds = { "sounds": all_sounds } #iteration complete, add all sounds to sounds dictionary
		self.write(json.dumps(sounds, default=json_util.default)) #write json
		self.finish() #finish

class MapHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*") 
		self.render("map.html")

class ReceiveJSONHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('ready to receive json')
	def post(self):
		data_json = tornado.escape.json_decode(self.request.body)
		coll = self.application.db.sounds
		sound = dict()
		sound['latitude'] = data_json['latitude']
		sound['longitude'] = data_json['longitude']
		sound['sound_url'] = foundling_aws_base_url + "sound_" + data_json['sound_date'] + ".wav"
		print sound
		coll.insert(sound)
		#print data_json
		#self.redirect('/receivejson')

if __name__ == "__main__":
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

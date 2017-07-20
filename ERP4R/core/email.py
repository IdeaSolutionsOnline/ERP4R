# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"

import os, sys
sys.path.append(os.getcwd())
from utils import *
import objs
from auth import verify_form_rights, require_auth
import bottle
import poplib
import email
import mimetypes
import random
import base64
from dateutil.parser import parse
from erp_config import style as style


class Receive_POP3(object):
	def __init__(self):
		self.context = get_base_context()
		self.savedir="/var/www/core/static/attachments/{project}/{user}".format(project=self.context['db_name'], user = self.context['user_name'])
		if not os.path.exists(self.savedir):
			os.makedirs(self.savedir)
		self.email = objs.emails.Emails()
		self.email_boxes = objs.email_account.EmailAccount(where="users = '{user}'".format(user=self.context['user'])).get()
		self.attachment = objs.attachment.Attachment()

	def save_message(self):
		if self.email_boxes[0] > 0:
			for box in self.email_boxes[1]:
				pop3_server = box['pop3_server']
				pop3_port = box['pop_port']
				pop3_user = box['pop_user']
				pop3_passw = base64.decodestring(box['pop_pass'].encode('utf-8')).decode('utf-8')[6:]
				#try:
				#print ('----------------------', type(box['ssl']), str(box['ssl']))
				if box['ssl'] == True:
					self.pop3_connection = poplib.POP3_SSL(pop3_server, pop3_port)
				else:
					self.pop3_connection = poplib.POP3(pop3_server, pop3_port)
				self.pop3_connection.set_debuglevel(0)
				self.pop3_connection.user(pop3_user)
				self.pop3_connection.pass_(pop3_passw)
				emails, total_bytes = self.pop3_connection.stat()
				#print("{0} emails in the inbox, {1} bytes total".format(emails, total_bytes))
				# return in format: (response, ['mesg_num octets', ...], octets)
				#msg_list = self.connection.list()
				#print(msg_list)
				# messages processing
				for i in range(emails):
					# return in format: (response, ['line', ...], octets)
					response = self.pop3_connection.retr(i+1)
					#print ('response', response)
					raw_message = response[1]
					#print (raw_message)
					str_message = email.message_from_bytes(b'\n'.join(raw_message))
#					msg = open(os.path.join(self.savedir, str(i)), 'wb')
#					msg.write(b'\n'.join(raw_message))
#					msg.close()
					#print (str_message)
					# save attach
					message_body = None
					message_header = str_message.items()
					#print (str_message.items())
					#if str_message.is_multipart();
						#é só uma mensagem simples de texto
					#else:
						#tem várias partes
					#attach(payload)utilizar em forward
					#get_payload(i, decode=True)devolve o payload que pode ser uma lista de mensagens se ultipart ou uma mensagem
					counter = 1
					attachment_file_names = {}
					for part in str_message.walk():
						#print (part)
						#print ('cabecalho', part.items())
						#print ('este e o content_type da part', part.get_content_type())
						typ = part.get_content_type()
						if typ and typ.lower() == "text/html": 
							# Found the first text/plain part 
							message_body = part.get_payload()
						if typ and typ.lower() == "text/plain": 
							if not message_body:
								message_body = part.get_payload()
						# multipart/* are just containers
						if part.get_content_maintype() == 'multipart':
							continue
						#if part.get('Content-Disposition') is None:
							#print("no content dispo")
						#	continue
						filename = part.get_filename()
						if not(filename):
							ext = mimetypes.guess_extension(part.get_content_type())
							if not ext:
							# Use a generic bag-of-bits extension
								ext = '.bin'
							filename = 'part-%03d%s' % (counter, ext)
							counter += 1
						else:
							if '.' in filename:
								ext = filename.split('.')[-1]
							else:
								ext = '.bin'
						#ao filename acrescento um random de 20 digitos para garantir que não perco ficheiros necessários, depois tambem dividir por directorias por projecto e por user
						readable_filename = filename
						filename = str(random.randint(1000000000000000000000000000000000000000, 9999999999999999999999999999999999999999)) + filename
						#print('my filename is ', filename)
						#print(part.get_payload(decode=1))
						part_header_list = part.items()
						part_header = {}
						for h in part_header_list:
							part_header[h[0]] = h[1]
						#print (part_header)
						if 'Content-ID' in part_header:
							attachment_file_names[part_header['Content-ID'].replace('<','').replace('>','')] = (readable_filename, filename)
						elif 'X-Attachment-Id' in part_header:
							attachment_file_names[part_header['X-Attachment-Id']] = (readable_filename, filename)
						if ext in ['.html', '.ksh']:
							pass
						else:
							data = part.get_payload(decode=True)
							fp = open(os.path.join(self.savedir, filename), 'wb')
							fp.write(data)
							fp.close()
					header_dict = {'Bcc':'', 'Date':'', 'Subject':'', 'From':'', 'To':'', 'Cc':'', 'Time':''}
					#for key in ['Bcc', 'Date', 'Subject', 'From', 'To', 'Cc']:
					for item in message_header:
						for key in ['Bcc', 'From', 'To', 'Cc']:
							if item[0] == key:
								if '<' in item[1]:
									header_dict[item[0]] = item[1].split('<')[1][:-1]
								else:
									header_dict[item[0]] = item[1]
						if item[0] == 'Date':
							#from datetime import datetime
							#datetime.strptime(item[1], '%a, %d %b %Y %H:%M:%S %z')
							#print (email.utils.parsedate_tz(item[1]))
							Data = parse(item[1])
							Time = parse(item[1])
						if item[0] == 'Subject':
							header_dict[item[0]] = item[1]
					#print (attachment_file_names)
					#print ('message body antes', message_body)
					#print (message_body)
					for file_name in attachment_file_names:
						#print (file_name)
						message_body = message_body.replace('cid:' + file_name,"/static/attachments/{project}/{user}/{file_name}".format(project=self.context['db_name'], user = self.context['user_name'], file_name = attachment_file_names[file_name][1]))
					#print ('message body depois', message_body)
					kargs = {'estado':'Novo', 'users':self.context['user'], 'date':Data, 'time':Time, 'msg_from':header_dict['From'], 'msg_to':header_dict['To'], 'cc':header_dict['Cc'], 'bcc':header_dict['Bcc'], 'subject':header_dict['Subject'], 'message':message_body, 'user':self.context['user']}
					self.email.kargs = kargs
					email_id = self.email.put()
					for file_name in attachment_file_names:
						kargs = {'model':self.email.__model_name__, 'model_id':email_id, 'attachment':"/static/attachments/{project}/{user}/{file_name}".format(project=self.context['db_name'], user = self.context['user_name'], file_name = attachment_file_names[file_name][1]), 'description':attachment_file_names[file_name][0], 'user':self.context['user']}
						self.attachment.kargs = kargs
						self.attachment.put()
				self.pop3_connection.quit()
#				except:
#					print ('Uma das contas de email está mal configurada!!!! ou não temos ligação para a internet!!!')

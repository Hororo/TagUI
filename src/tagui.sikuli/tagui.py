# SIKULI INTERFACE FOR TAGUI FRAMEWORK ~ TEBEL.ORG #

# timeout in seconds for finding an element
wait_timeout = 10
setAutoWaitTimeout(wait_timeout)

# delay in seconds between scanning for inputs
scan_period = 0.5

# counter to track current tagui sikuli step
tagui_count = '0'

# prevent premature exit on unhandled exception
setThrowException(False)

# enable OCR (optical character recognition)
Settings.OcrTextRead = True
Settings.OcrTextSearch = True

# helper function to detect coordinates locator
def is_coordinates ( input_locator ):
	if input_locator[:1] == '(' and input_locator[-1:] == ')' and input_locator.count(',') == 1:
		return True
	else:
		return False

# helper function to return x coordinate from (x,y)
def x_coordinate ( input_locator ):
	return int(input_locator[1:input_locator.find(',')])

# helper function to return y coordinate from (x,y)
def y_coordinate ( input_locator ):
        return int(input_locator[input_locator.find(',')+1:-1])

# function to output sikuli text to tagui
def output_sikuli_text ( output_text ):
	import codecs
	tagui_text = codecs.open('tagui.sikuli/tagui_sikuli.txt','w',encoding='utf8')
	tagui_text.write(output_text)
	tagui_text.close()

# function for tap / click step
def tap_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - click ' + params
	if is_coordinates(params):
		return click(Location(x_coordinate(params),y_coordinate(params)))
	elif exists(params):
		return click(params)
	else:
		return 0

# function for rtap / rclick step
def rtap_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - rclick ' + params
	if is_coordinates(params):
		return rightClick(Location(x_coordinate(params),y_coordinate(params)))
	elif exists(params):
		return rightClick(params)
	else:
		return 0

# function for dtap / dclick step
def dtap_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - dclick ' + params
	if is_coordinates(params):
		return doubleClick(Location(x_coordinate(params),y_coordinate(params)))
	elif exists(params):
		return doubleClick(params)
	else:
		return 0

# function for hover / move step
def hover_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - hover ' + params
	if is_coordinates(params):
		return hover(Location(x_coordinate(params),y_coordinate(params)))
	elif exists(params):
		return hover(params)
	else:
		return 0

# function for type / enter step
def type_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	param1 = params[:params.find(' as ')].strip()
	param2 = params[4+params.find(' as '):].strip()
	print '[tagui] ACTION - type ' + param1 + ' as ' + param2
	param2 = param2.replace('[enter]','\n')
	param2 = param2.replace('[clear]','\b')
	if param1.endswith('page.png') or param1.endswith('page.bmp'):
		return type(param2)
	elif is_coordinates(param1):
		return type(Location(x_coordinate(param1),y_coordinate(param1)),param2)
	elif exists(param1):
		return type(param1,param2) 
	else:
		return 0

# function for select / choose step
def select_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	param1 = params[:params.find(' as ')].strip()
	param2 = params[4+params.find(' as '):].strip()
	print '[tagui] ACTION - click ' + param1
	if is_coordinates(param1):
		if click(Location(x_coordinate(param1),y_coordinate(param1))) == 0:
			return 0
		else:
			print '[tagui] ACTION - click ' + param2
			if is_coordinates(param2):
				return click(Location(x_coordinate(param2),y_coordinate(param2)))
			elif exists(param2):
				return click(param2)
			else:
				return 0
 
	elif exists(param1):
		if click(param1) == 0:
			return 0
		else:
			print '[tagui] ACTION - click ' + param2
			if is_coordinates(param2):
				return click(Location(x_coordinate(param2),y_coordinate(param2)))
			elif exists(param2):
				return click(param2)
			else:
				return 0
	else:
		return 0

# function for reading OCR text
def read_intent ( raw_intent ):
	return text_read(raw_intent)

# function for showing OCR text
def show_intent ( raw_intent ):
	return text_read(raw_intent)

# function for saving OCR text
def save_intent ( raw_intent ):
	return text_read(raw_intent)

# function for reading text using Tesseract OCR
def text_read ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	param1 = params[:(params + ' ').find(' ')].strip()

	print '[tagui] ACTION - ' + raw_intent
	if param1.endswith('page.png') or param1.endswith('page.bmp'):
		fullscreen_layer = Screen()
		temp_text = fullscreen_layer.text()
		output_sikuli_text(temp_text)
		return 1
	elif exists(param1):
		matched_element = find(param1)
		temp_text = matched_element.text()
		output_sikuli_text(temp_text)
		return 1
	else:
		return 0

# function for capturing screenshot
def snap_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	param1 = params[:params.find(' to ')].strip()
	param2 = params[4+params.find(' to '):].strip()
	print '[tagui] ACTION - snap ' + param1 + ' to ' + param2
	if param1.endswith('page.png') or param1.endswith('page.bmp'):
		fullscreen_layer = Screen()
		temp_snap_file = fullscreen_layer.capture(fullscreen_layer.getBounds()).getFile()
		import shutil
		shutil.copy(temp_snap_file,param2)
		return 1
	elif exists(param1):
		fullscreen_layer = Screen()
		matched_element = find(param1)
		temp_snap_file = fullscreen_layer.capture(matched_element).getFile()
		import shutil
		shutil.copy(temp_snap_file,param2)
		return 1
	else:
		return 0

# function for low-level mouse control
def mouse_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - mouse ' + params
	if params.lower() == 'down':
		hover(Location(Env.getMouseLocation().getX(),Env.getMouseLocation().getY()))
		mouseDown(Button.LEFT)
		return 1
	elif params.lower() == 'up':
		hover(Location(Env.getMouseLocation().getX(),Env.getMouseLocation().getY()))
		mouseUp(Button.LEFT)
		return 1
	else:
		return 0

# function for sending custom commands
def vision_intent ( raw_intent ):
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - ' + params
	exec(params,globals())
	return 1
	
def visible_intent ( raw_intent ):
	setAutoWaitTimeout(1)
	params = (raw_intent + ' ')[1+(raw_intent + ' ').find(' '):].strip()
	print '[tagui] ACTION - ' + raw_intent.strip()
	if exists(params):
		setAutoWaitTimeout(wait_timeout)
		return 1
	else:
		setAutoWaitTimeout(wait_timeout)
		return 0

# function to interpret input intent
def get_intent ( raw_intent ):
	if raw_intent[:4].lower() == 'tap ' or raw_intent[:6].lower() == 'click ':
		return 'tap'
	if raw_intent[:5].lower() == 'rtap ' or raw_intent[:7].lower() == 'rclick ':
		return 'rtap'
	if raw_intent[:5].lower() == 'dtap ' or raw_intent[:7].lower() == 'dclick ':
		return 'dtap'
	if raw_intent[:6].lower() == 'hover ' or raw_intent[:5].lower() == 'move ': 
		return 'hover'
	if raw_intent[:5].lower() == 'type ' or raw_intent[:6].lower() == 'enter ': 
		return 'type'
	if raw_intent[:7].lower() == 'select ' or raw_intent[:7].lower() == 'choose ':
		return 'select'
	if raw_intent[:5].lower() == 'read ' or raw_intent[:6].lower() == 'fetch ':
		return 'read'
	if raw_intent[:5].lower() == 'show ' or raw_intent[:6].lower() == 'print ':
		return 'show'
	if raw_intent[:5].lower() == 'save ':
		return 'save'
	if raw_intent[:5].lower() == 'snap ':
		return 'snap'
	if raw_intent[:6].lower() == 'mouse ':
		return 'mouse'
	if raw_intent[:7].lower() == 'vision ':
		return 'vision'
	if raw_intent[:8].lower() == 'visible ' or raw_intent[:8].lower() == 'present ':
		return 'visible';
	return 'error'

# function to parse and act on intent
def parse_intent ( script_line ):
	intent_type = get_intent(script_line)
	if intent_type == 'tap':
		return tap_intent(script_line)
	elif intent_type == 'rtap':
		return rtap_intent(script_line)
	elif intent_type == 'dtap':
		return dtap_intent(script_line)
	elif intent_type == 'hover':
		return hover_intent(script_line)
	elif intent_type == 'type':
		return type_intent(script_line)
	elif intent_type == 'select':
		return select_intent(script_line)
	elif intent_type == 'read':
		return read_intent(script_line)
	elif intent_type == 'show':
		return show_intent(script_line)
	elif intent_type == 'save':
		return save_intent(script_line)
	elif intent_type == 'snap':
		return snap_intent(script_line)
	elif intent_type == 'mouse':
		return mouse_intent(script_line)
	elif intent_type == 'vision':
		return vision_intent(script_line)
	elif intent_type == 'visible':
		return visible_intent(script_line);
	else:
		return 0 

# write to interface out-file to signal ready for inputs
tagui_output = open('tagui.sikuli/tagui_sikuli.out','w')
tagui_output.write('[0] START')
tagui_output.close()

# initialise interface in-file before starting main loop
tagui_input = open('tagui.sikuli/tagui_sikuli.in','w')
tagui_input.write('')
tagui_input.close()

# main loop to scan inputs from automation flow
print '[tagui] START  - listening for inputs'; print
while True:
	# scan input from run-time interface in-file
	try:
		tagui_input = open('tagui.sikuli/tagui_sikuli.in','r')
	except IOError, OSError:
		print '[tagui] ERROR  - cannot open tagui.sikuli/tagui_sikuli.in'; print
		break
	tagui_intent = tagui_input.read().strip()
	tagui_input.close()

	# quit if finish signal received, initialise and repeat loop if blank
	if tagui_intent == 'finish':
		break
	elif not tagui_intent:
		tagui_count = '0'
		tagui_output = open('tagui.sikuli/tagui_sikuli.out','w')
		tagui_output.write('[0] START')
		tagui_output.close()
		wait(scan_period)
		continue

	# get count and repeat loop if same count as last iteration
	temp_count = tagui_intent[1:tagui_intent.find('] ')].strip()
	tagui_intent = tagui_intent[2+tagui_intent.find('] '):].strip()
	if tagui_count == temp_count:
		wait(scan_period)
		continue
	else:
		tagui_count = temp_count

	# otherwise parse and act on input intent
	print '[tagui] INPUT  - ' + '[' + tagui_count + '] ' + tagui_intent 
	intent_result_value = parse_intent(tagui_intent)
	if intent_result_value == 1:
		intent_result_string = 'SUCCESS'
	else:
		intent_result_string = 'ERROR'

	# save intent_result to interface out-file
	print '[tagui] OUTPUT - ' + '[' + tagui_count + '] ' + intent_result_string; print
	tagui_output = open('tagui.sikuli/tagui_sikuli.out','w')
	tagui_output.write('[' + tagui_count + '] ' + intent_result_string)
	tagui_output.close()
	wait(scan_period)

# write to interface out-file to signal finish listening
print '[tagui] FINISH - stopped listening'
tagui_output = open('tagui.sikuli/tagui_sikuli.out','w')
tagui_output.write('[0] FINISH')
tagui_output.close()

extends Sprite2D

func _input(event):
	# move the sprite to the mouse position
	# if the mouse button is clicked
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		position = event.position

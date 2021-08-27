def get_integer(prompt = "Enter an Integer: ", error = "Invalid Integer", error_for_float = "Number needs to be integer not float"):
	while True:
		try:
			num = input(prompt)
			num = float(num)
			if float(int(num)) == num:
				return int(num)
			else:
				print(error_for_float)
		except ValueError:
			print(error)


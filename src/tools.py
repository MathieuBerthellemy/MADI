import math

def compute_gamma(width, height, R):
		D = width+height

		output = 0.5
		output_bounds = (0, 1)

		window = (5, 10)
		while True:

			tmp = R
			for i in range(int(D/4)):
				tmp = math.pow(tmp, output)
		
			# Si en dessous de la fenetre
			if tmp < window[0]:
				output_bounds = (output, output_bounds[1])

			# S au dessus de la fenetre
			elif tmp > window[1]:
				output_bounds = (output_bounds[0], output)
			# Si dans la fenetre
			else:
				break

			output = (output_bounds[0] + output_bounds[1])/2
			#print output, ": ", output_bounds, ", ", tmp

		#print "gamma = ", output
		return min(output, 0.8)

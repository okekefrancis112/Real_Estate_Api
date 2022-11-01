import shortuuid

def get_ip(request):
	try:
		x_forward=request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip=x_forward.split(",")[0]
		else:ip= request.META.get("REMOTE_ADDR")
	except:
			ip=""
	return ip


def generate_referral_code():
        return shortuuid.ShortUUID().random(length=13)


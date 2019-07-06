with open('client.log') as f:
    with open('success.log', mode='w') as o:
        for line in f:
            try:
                if line[0:6] != '[INFO]':
                    continue
                _, _, _, _, line = line.split(' - ', maxsplit=4)
                if line.find('Miner') > 0:
                    o.write(line)
            except Exception as e:
                print(e)

with open('brute.log') as f:
    with open('success.log', mode='w') as o:
        for line in f:
            try:
                if line.find('SUCCESS') > 0:
                    o.write(line)
            except Exception as e:
                print(e)

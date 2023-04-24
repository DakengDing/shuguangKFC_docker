
class Trans:




    def parseFleet(data):
        members = {}
        lines = data.split('\n')
        for line in lines:
            fields = line.strip().split('\t')
            keys = fields[0]
            location = fields[1].replace(' (已停靠)', '')
            member = {
                'location':location,
                'ship':fields[2],
                'ship_type':fields[3],
                'role':fields[4]
            }
            members[keys]=member



        #print(members)
        return members


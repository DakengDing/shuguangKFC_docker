
class Trans:




    def parseFleet(data):
        members = {}
        lines = data.split('\n')
        # print(len(lines))
        for line in lines:
            # print(line)
            
            fields = line.strip().split('\t')
            # print(len(fields))
            if len(fields)<= 2:
                continue
            keys = fields[0]
            location = fields[1].replace(' (已停靠)', '')
            member = {
                'location':location,
                'ship':fields[2],
                'ship_type':fields[3],
                'role':fields[4]
            }
            members[keys]=member
            # print(member)



        
        return members


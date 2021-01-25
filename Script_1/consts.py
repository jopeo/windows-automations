
# All constants from big_boi.py should be listed here:

log_path = 'F://yourpath'

xpath = """
<QueryList>
    <Query Id="0" Path="Security">
        <Select Path="Security">
            *[System[(EventID=4663 or EventID=4656)]]
            and
            *[EventData[Data[@Name='AccessMask'] and (Data='0x2' or Data='0x4' or Data='0x4' or Data='0x10' or Data='0x40' or Data='0x100' or Data='0x1000')]]
        </Select>
        <Suppress Path="Security">
            *[EventData[Data[@Name='ObjectName'] and Data='\\\yourpath']]
        </Suppress>
    </Query>
</QueryList>
"""

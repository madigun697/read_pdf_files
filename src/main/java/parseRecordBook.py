import re
import collections
import os
import pymysql

korean_pattern = re.compile('[가-힣]*')
number_pattern = re.compile('[0-9]*')
game_seq_pattern = re.compile('경기번호: [0-9]*')

# no_sub
p1 = "(\d+)\s(\d+)\s([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)(\d)(\d)(\d)\s(\d)\s(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)\s(\d)([A-z]+)(\d+)([A-z]+)(\d)\s(\d)(\d)"
# sub_1
p2 = "(\d+)\s(\d+)\s([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)(\d)(\d)(\d)\s(\d)\s(\d)(\d)(\d)(\d)(\d)(\d)(\d)([가-힣]+\d+\W\d+\W)(\d)\s(\d)([A-z]+)(\d)([A-z]+)(\d)\s(\d)(\d)"
# sub_2
p3 = "(\d+)\s(\d+)\s([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)(\d)(\d)(\d)\s(\d)\s(\d)(\d)(\d)(\d)(\d)(\d)(\d)([가-힣]+\d+\W\d+\W)\s([가-힣]+\d+\W\d+\W)(\d)\s(\d)([A-z]+)(\d)([A-z]+)(\d)\s(\d)(\d)"
# sub_no_sub
p4 = "(\d+)\s(\d+)\s([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)(\d)(\d)(\d)\s(\d)\s(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)\s(\d)([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)"
# sub_sub_1
p5 = "(\d+)\s(\d+)\s([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)(\d)(\d)(\d)\s(\d)\s(\d)(\d)(\d)(\d)(\d)(\d)(\d)([가-힣]+\d+)\s(\d)([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)"
# sub_sub_2
p6 = "(\d+)\s(\d+)\s([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)(\d)(\d)(\d)\s(\d)\s(\d)(\d)(\d)(\d)(\d)(\d)(\d)([가-힣]+\d+)\s([가-힣]+\d+)\s(\d)([가-힣]+)(\d+)([가-힣]+)(\d)\s(\d)(\d)"

pattern_list = [p1, p2, p3, p4, p5, p6]

headers_27 = ['unknown1', 'away_nuumber', 'away_name', 'home_number', 'home_name', 'unknown2', 'home_ST', 'home_OS', \
              'home_FC', 'home_CK', 'home_GL', 'home_AS', 'unknown3', 'away_ST', 'away_OS', 'away_FC', 'away_CK', \
              'away_AS', 'away_GL', 'home_FS', 'away_FS', 'away_position', 'seq', 'home_position', 'home_YC', \
              'unknown4', 'away_YC']

headers_28 = ['unknown1', 'away_nuumber', 'away_name', 'home_number', 'home_name', 'unknown2', 'home_ST', 'home_OS', \
              'home_FC', 'home_CK', 'home_GL', 'home_AS', 'unknown3', 'away_ST', 'away_OS', 'away_FC', 'away_CK', \
              'away_AS', 'away_GL', 'sub1', 'home_FS', 'away_FS', 'away_position', 'seq', 'home_position', 'home_YC', \
              'unknown4', 'away_YC']

headers_29 = ['unknown1', 'away_nuumber', 'away_name', 'home_number', 'home_name', 'unknown2', 'home_ST', 'home_OS', \
              'home_FC', 'home_CK', 'home_GL', 'home_AS', 'unknown3', 'away_ST', 'away_OS', 'away_FC', 'away_CK', \
              'away_AS', 'away_GL', 'sub1', 'sub2', 'home_FS', 'away_FS', 'away_position', 'seq', 'home_position', \
              'home_YC', 'unknown4', 'away_YC']

file_list = os.listdir('./txts/')
file_list.sort()


def get_game_detail():
    game_record_books = []

    for txt in file_list:
        f = open('./txts/' + txt, encoding='utf-8')
        sub_judge = []
        player = []
        for idx, line in enumerate(f.readlines()):
            if idx == 2:
                game_year = line.split(' ')[1].replace('\n', '')
            if idx == 3:
                game_seq = game_seq_pattern.findall(line)[0].split(':')[1].replace('\n', '').strip()
            if idx == 5:
                game_supervisor = line.split('경기감독관')[0].replace('\n', '')
            if idx == 6:
                line_parse = line.split('주  심')
                main_judge = line_parse[0].replace('\n', '')
                away_team = line_parse[1].split('전반')[0]
                away_team_name = away_team[0:len(away_team) - 1]
                away_team_score_1 = away_team[len(away_team) - 1]
                home_team = line_parse[1].split('전반')[1]
                home_team_name = home_team[1:len(home_team) - 1]
                home_team_score_1 = home_team[0]
            if idx == 7:
                audiences = line.split(' ')[1]
            if idx == 8:
                judge_supervisor = line.split('심판감독관')[0].replace('\n', '')
            if idx == 9:
                sub_judge.append(line.replace('\n', ''))
            if idx == 11:
                line_parse = line.split(' ')
                if line_parse[1] == '':
                    l = line_parse[2].split('후반')
                    away_team_score_2 = l[0][0]
                    home_team_score_2 = l[1][0]
                    first_kick_team = 'home'
                else:
                    l = line_parse[1].split('후반')
                    away_team_score_2 = l[0][2]
                    home_team_score_2 = l[1][0]
                    first_kick_team = 'away'
            if idx == 14:
                sub_judge.append(line.replace('\n', ''))
            if idx == 15:
                recorder = line.split(' ')[1].replace('\n', '')
            if idx == 17:
                weather = line.split(')')[1].replace('\n', '')
            if idx == 18:
                stand_by_judge = line.split('대기심')[0]
            if idx in range(22, 40):
                for pattern in pattern_list:
                    p = re.compile(pattern)
                    m = p.search(line)
                    if m != None:
                        player.append(m)
                        break

        player_activity = []
        for p in player:
            p_dict = collections.OrderedDict()
            if p.lastindex == 27:
                headers = headers_27
            elif p.lastindex == 28:
                headers = headers_28
            elif p.lastindex == 29:
                headers = headers_29

            for i in range(1, p.lastindex):
                p_dict[headers[i - 1]] = p.group(i)
            player_activity.append(p_dict)

        game_record_book = \
            {'game_year': game_year, 'game_division': 1, 'game_seq': game_seq, 'weather': weather,
             'game_supervisor': game_supervisor, 'judge_supervisor': judge_supervisor, 'recorder': recorder,
             'main_judge': main_judge, 'sub_judge_1': sub_judge[0], 'sub_judge_2': sub_judge[1],
             'stand_by_judge': stand_by_judge, 'audiences': audiences, 'first_kick_team': first_kick_team,
             'home_team_name': home_team_name, 'away_team_name': away_team_name, 'home_team_score_1': home_team_score_1,
             'home_team_score_2': home_team_score_2, 'away_team_score_1': away_team_score_1,
             'away_team_score_2': away_team_score_2, 'player_activity': player_activity}

        game_record_books.append(game_record_book)

    return game_record_books


def get_team_id(conn, team_name):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = """select team_id from team_info where team_name = '%s'""" % team_name
    curs.execute(sql)
    result = curs.fetchall()
    team_id = -1
    for r in result:
        team_id = r['team_id']

    return team_id


def update_table(params):
    print(params)
    sql = """UPDATE game_records_expand SET weather = %s, game_supervisor = %s, judge_supervisor = %s, recorder = %s, 
        main_judge = %s, sub_judge_1 = %s, sub_judge_2 = %s, stand_by_judge = %s, audiences = %s, first_kick_team = %s
        WHERE game_id = %s """
    curs = conn.cursor()
    curs.executemany(sql, tuple(params))
    conn.commit()


conn = pymysql.connect(host='madigun.asuscomm.com', user='madigun', password='ehenr1163', db='football', charset='utf8')
params = []
for book in get_game_detail():
    match_id = '%s-%s-%s' % (book['game_year'], book['game_division'], book['game_seq'].zfill(3))

    if book['first_kick_team'] == 'home':
        first_kick_team = book['home_team_name']
    else:
        first_kick_team = book['away_team_name']

    params.append((book['weather'], book['game_supervisor'], book['judge_supervisor'], book['recorder'],
                   book['main_judge'], book['sub_judge_1'], book['sub_judge_2'], book['stand_by_judge'],
                   int(book['audiences']), get_team_id(conn, first_kick_team), match_id))


update_table(params)

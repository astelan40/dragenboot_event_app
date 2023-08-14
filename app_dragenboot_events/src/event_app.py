from flask import Flask, render_template
import event_parser

db_app = Flask(__name__)

@db_app.route('/2023/hameln')
def hameln_results():
    sorted_times = event_parser.parse_dragenboat_online_events('19-hamelner-fun-regatta', 'a96a85788301493da4d7546dd806d297', ['Zeitlauf'])
    max_num_races = event_parser.max_num_races(sorted_times)
    return render_template('results_template.html', event_name = '19. Hamelner Fun-Regatta', sorted_times=sorted_times, max_num_races = max_num_races)

@db_app.route('/2023/schwerin')
def schwerin_results():
    sorted_times = event_parser.parse_dragenboat_online_events('schweriner-drachenbootfestival-2023', 'a52a92170eb64ab5a654f7ea3feeecfb', ['Wertungslauf'])
    max_num_races = event_parser.max_num_races(sorted_times)
    return render_template('results_template.html', event_name = 'Schweriner Drachenbootfestival 2023 - Business Races', sorted_times=sorted_times, max_num_races = max_num_races)

@db_app.route('/2023/hannover')
def hannover_results():
    sorted_times = event_parser.parse_dragenboat_online_events('drachenbootfestival-hannover-2023', '887cbe6fa2e74d8ba669796a32766cc2', ['Fun Sport', 'Zeitrennen'])
    max_num_races = event_parser.max_num_races(sorted_times)
    return render_template('../templates/results_template.html', event_name = 'Drachenbootfestival Hannover 2023 - Fun Sport', sorted_times=sorted_times, max_num_races = max_num_races)


if __name__ == '__main__':
    db_app.run()

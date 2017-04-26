function time_min = timeViewToMin( t_str )
%TIMEVIEWTOMIN( t_str ) Translates from the format m-s-f to a double in
%minutes
%   TIMEVIEWTOMIN( t_str ) Takes a string of the format m-s-f and returns a
%   double with the corresponding value in minutes. E.g. if t_str =
%   10-30-0, time_min = 10.5.
    t_str_split = strsplit(t_str, '-');
    t_min = str2double(t_str_split{1});
    t_sec = str2double(t_str_split{2});
    t_tho = str2double(t_str_split{3});
    
    time_min = t_min + t_sec/60 + t_tho/60000;

end


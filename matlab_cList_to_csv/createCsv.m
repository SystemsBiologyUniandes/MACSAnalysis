function createCsv(time_dir, csv_filename )
%CREATECSV Appends the cLists for each time to the csv
%   CREATECSV(time_dir, csv_filename) Appends the csv file with the data in
%   all the cLists corresponding to a fixed time (inside time_dir).
%       time_dir must correspond to some time directory, it should end e.g.
%       as /t90-92 and contain the directories xy01, xy02, ...
%       csv_filename must be the complete path of the csv file (including
%       the. csv extension).
    dir_list = listDirectories(time_dir);
    
    % REMOVED V3
    %addHeaderCsv(dir_list{1}, csv_filename);
    
    for i = 1:length(dir_list)
        addDataCsv(dir_list{i}, csv_filename);
    end
end
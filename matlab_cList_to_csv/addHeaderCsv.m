function addHeaderCsv(pos_path, filename )
%ADDHEADERCSV Creates a csv file and adds the corresponding header 
%   ADDHEADERCSV(pos_path, filename) Creates a csv file named filename and
%   adds the header corresponding to the def3D element of the clist.mat
%   file inside path.
%       path must correspond to a position inside some time directory, it
%       should end e.g. as /t90-92/xy01/ (WITH THE FINAL / ).
%       filename must be the complete path of the csv file. (including the
%       .csv extension).
    file_csv = fopen(filename, 'w');
    full_filename = strcat(pos_path,'clist.mat');
    c1 = load(full_filename);
    
    % NEW v3
    fprintf(file_csv, '%s,', 'time(min)');
    
    % NEW V2
    fprintf(file_csv, '%s,', 'xy');
    fprintf(file_csv, '%s,',c1.def3D{1:end-1});
    fprintf(file_csv, '%s\n',c1.def3D{1,end});
    fclose(file_csv);
end


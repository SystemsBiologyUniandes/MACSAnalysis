function addDataCsv( pos_path, filename )
%ADDDATACSV Adds the data to the existent csv file
%   ADDDATACSV( pos_path, filename ) Adds the data to the csv file inside
%   path that has been created using addHeaderCsv(pos_path, filename). The
%   data correspond to the data3D element of the clist.mat file located
%   inside pos_path.
%       pos_path must correspond to a position inside some time directory, 
%       it should end e.g. as /t90-92/xy01/ (WITH THE FINAL / ).
%       filename must be the complete path of the csv file (including the
%       .csv extension)

    full_filename = strcat(pos_path,'clist.mat');
    c1 = load(full_filename);
    n_rows = size(c1.data3D, 1);
    
    % UNCOMMENT TO EXCLUDE SELECTED CELLS
    %n_cols = size(c1.data3D, 2);
      
%     try
%         c_new = zeros(n_rows - length(c1.idExclude), n_cols);
%         i_new = 1;
%         for i = 1:n_rows
%             if ~any(c1.idExclude == i)
%                 c_new(i_new,:) = c1.data3D(i,:);
%                 i_new=i_new+1;
%             end
%         end
%         n_rows = n_rows - length(c1.idExclude);    
%     catch
    c_new = c1.data3D;
%     end
    
    % NEW Extracts the position from the dir name
    pos_split = strsplit(pos_path, '/');
    xy = str2double(pos_split{end-1}(3:end));
    c_xy = xy*ones(n_rows, 1);
    
    % NEW V3 ADD TIME DATA
    time_str = pos_split{end-2};
    time_min = timeViewToMin(time_str);
    c_time = time_min*ones(n_rows, 1);
    
    % NEW Merges columns
    c_full = [c_time, c_xy, c_new];
    
    % Write file
    dlmwrite(filename, c_full, '-append');
end

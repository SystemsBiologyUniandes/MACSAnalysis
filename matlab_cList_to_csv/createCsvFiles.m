function createCsvFiles( experiment_dir )
%CREATECSVFILES Creates a unique csv files corresponding to the experiment.
%   CREATECSVFILES(experiment_dir) Creates the csv files corresponding to
%   the experiment.
%       experiment_dir must correspond to the experiment directory i.e. it
%       must ONLY contain the time folders. THE LAST / MUST BE INCLUDED.
%       The csv file is stored in the experiment directory and its name is
%       the same as the experiment directory's.

    a = dir(experiment_dir);
    
    % NEW extract experiment name
    exp_dir_split = strsplit(experiment_dir, '/');
    experiment_name = exp_dir_split{end-1};
    
    % NEW V3 FIND THE HEADERS IN THE FIRST XY OF THE FIRST TIME AND ADDS
    csv_filename = strcat(experiment_dir,experiment_name,'.csv');
    time_dir_full = strcat(experiment_dir, a(3).name, '/');
    pos_dirs = listDirectories(time_dir_full);
 
    for i = 3:length(a)
        createCsv(strcat(experiment_dir,a(i).name), csv_filename);
    end
    
    csv_unsorted = csvread(csv_filename);
    
    % NEW V3 SORT CSV
    [~, order] = sort(csv_unsorted(:,1));
    csv_sorted = csv_unsorted(order,:);
    addHeaderCsv(pos_dirs{1}, csv_filename);
    dlmwrite(csv_filename, csv_sorted,'-append');
end
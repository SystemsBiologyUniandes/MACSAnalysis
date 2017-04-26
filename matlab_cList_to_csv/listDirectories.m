function dir_list  = listDirectories( time_dir )
%LISTDIRECTORIES Returns a list with the position directories located
%inside the directory time_dir
%   LISTDIRECTORIES( time_dir ) Returns a list with the directories inside
%   time_dir that start with xy. This correspond to the directories that
%   SuperSegger creates after being executed.
    a = dir(time_dir);
    dir_list = {};
    for i = 3:length(a)
        if a(i).isdir == 1 && strncmpi(a(i).name,'xy',2)
            dir_list{end+1} = strcat(time_dir,'/',a(i).name,'/');
        end
    end
end


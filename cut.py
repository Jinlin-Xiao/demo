import os
from moviepy.editor import VideoFileClip


def change(movie_name, out_root_dir, out_dir):
    if movie_name in os.listdir(os.path.join(out_root_dir, out_dir)):
        count = 1
        movie_name = list(movie_name)
        movie_name.insert(-4, f"({count})")
        while ''.join(movie_name) in os.listdir(os.path.join(out_root_dir, out_dir)):
            count += 1
            movie_name[-5] = f"({count})"
        return ''.join(movie_name)
    return movie_name


def solve(f, movie_name, out_root_dir):
    out_action = {1: "crawl_", 2: 'rest_', 3: 'sit_'}
    out_time = {1: "inside_day", 2: "inside_night", 3: 'outside_day', 4: 'outside_night'}
    start_time = int(input("start_time(输入-1跳过不剪):"))
    if start_time == -1:
        print("----------跳过----------")
        return False
    during_time = int(input("during_time:"))
    target_action = int(input("(1: 'crawl_', 2: 'rest_', 3: 'sit_'):"))
    target_time = int(input("(1: 'inside_day', 2: 'inside_night', 3: 'outside_day', 4: 'outside_night'):"))
    clip = f.subclip(start_time, start_time + during_time)
    out_dir = out_action[target_action] + out_time[target_time]
    movie_name = change(movie_name, out_root_dir=out_root_dir, out_dir=out_dir)
    output_file = os.path.join(out_root_dir, out_dir, movie_name)
    clip.write_videofile(output_file)
    return True


class Movie:
    def __init__(self, root_dir, movie_dir):
        self.root_dir = root_dir
        self.movie_dir = movie_dir
        self.path = os.path.join(self.root_dir, self.movie_dir)
        self.movie_path = os.listdir(self.path)

    def __getitem__(self, idx):
        movie_name = self.movie_path[idx]
        movie_item_path = os.path.join(self.path, movie_name)
        f = VideoFileClip(movie_item_path)
        return f, movie_name


class Cut:
    def __init__(self, root_dir, movie_dir, out_root_dir, start_epoch, epoch):
        self.root_dir = root_dir
        self.movie_dir = movie_dir
        self.out_root_dir = out_root_dir
        self.start_epoch = start_epoch
        self.epoch = epoch
        self.movie = Movie(root_dir=self.root_dir, movie_dir=self.movie_dir)

    def run2(self):
        n = 0
        for step in range(self.start_epoch, self.start_epoch + self.epoch):
            f, movie_name = self.movie[step]
            print(f"------视频{n + 1}:{movie_name}------")
            if not solve(f, movie_name, self.out_root_dir):
                f.close()
                n += 1
                continue
            print("------------完成------------")
            flag = input("此视频是否还要再剪一个片段：[y/n]")
            while flag == 'y':
                if not solve(f, movie_name, self.out_root_dir):
                    f.close()
                    break
                print("------完成------")
                flag = input("此视频是否还要再剪一个片段：[y/n]")
            print("-------------------------------")
            n += 1
            f.close()


'''
仅需修改以下
root_dir       视频文件根目录
movie_dir      视频文件的目录
out_root_dir   输出的根目录
start_epoch    直接在硬盘上剪的：所需要剪的视频的第一个视频的序号 减 1   拷贝到自己电脑的：取0
epoch          该批次视频的数量  (直接在硬盘上剪的：需要剪的最后一个视频的序号 - 所需要剪的视频的第一个视频的序号 + 1)
                                拷贝到自己电脑的：直接全选查看文件数量
'''
# 假如原视频在F:\origin\神坪树\105neiwai  heshui里 剪辑视频放到F:\cut60
# --->>确保输出目录下已经创建好12个文件夹<<--
# --->>确保输出目录下已经创建好12个文件夹<<--
# --->>确保输出目录下已经创建好12个文件夹<<--
root_dir = r"F:\origin"
movie_dir = "209_106wai"
out_root_dir = r'F:\cut61'
start_epoch = 0
epoch = 33

cut = Cut(root_dir=root_dir, movie_dir=movie_dir, out_root_dir=out_root_dir, start_epoch=start_epoch,
          epoch=epoch)
cut.run2()

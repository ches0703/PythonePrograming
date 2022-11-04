
# Read File
def FReadData(file_name):
    st_data_list = []
    with open(file_name, "r") as file_student_records:
        st_data_liles = file_student_records.readlines()
    for line in st_data_liles:
        Name, Kor, Eng, Math, Sci = line.split()
        temp_list = [Name, Kor, Eng, Math, Sci]
        st_data_list.append(temp_list)
    return st_data_list


def FWriteData(file_name, st_data_list):
    with open(file_name, "w") as file_output:
        file_output.write("============================================\n")
        file_output.write("Name :  Kor   Eng  Math   Sci    Sum     Avg\n")
        for st_data in st_data_list:
            str_st_data = FormatingStudentData(st_data)
            file_output.write(str_st_data)
        file_output.write("============================================\n")


def CalcStudentList(st_data_list):
    for st_data in st_data_list:
        score_sum = 0
        for i in range(1, len(st_data)):
            score_sum += int(st_data[i])
        score_avg = score_sum / (len(st_data) - 1)
        st_data.append(score_sum)
        st_data.append(score_avg)


def CalEachClass(st_data_list):
    each_class_avg_list = {
        "Kor_avg": 0,
        "Eng_avg": 0,
        "Math_avg": 0,
        "Sci_avg": 0
    }
    for st_data in st_data_list:
        each_class_avg_list["Kor_avg"] += int(st_data[1])
        each_class_avg_list["Eng_avg"] += int(st_data[2])
        each_class_avg_list["Math_avg"] += int(st_data[3])
        each_class_avg_list["Sci_avg"] += int(st_data[4])

    each_class_avg_list["Kor_avg"] /= len(st_data_list)
    each_class_avg_list["Eng_avg"] /= len(st_data_list)
    each_class_avg_list["Math_avg"] /= len(st_data_list)
    each_class_avg_list["Sci_avg"] /= len(st_data_list)

    return each_class_avg_list


def FormatingStudentData(st_data):
    s = ""
    s += "{:<5}: ".format(st_data[0])  # Name
    s += "{:>4}, ".format(st_data[1])  # Kor
    s += "{:>4}, ".format(st_data[2])  # Eng
    s += "{:>4}, ".format(st_data[3])  # Math
    s += "{:>4}, ".format(st_data[4])  # Sci
    s += "{:>5}, ".format(st_data[5])  # Sum
    s += "{:>6.2f} ".format(st_data[6])  # Avg
    s += "\n"
    return s


def PrintStudentList(st_data_list):
    print("============================================")
    print("Name :  Kor   Eng  Math   Sci    Sum     Avg")
    for st_data in st_data_list:
        str_st_data = FormatingStudentData(st_data)
        print(str_st_data, end="")
    print("============================================")


if __name__ == "__main__":

    # File Relative Path
    input_file_name = "Weak09/student_records.txt"
    output_file_name = "Weak09/output.txt"

    # File Read and Print
    st_data_list = FReadData(input_file_name)
    for st_data in st_data_list:
        print(st_data)
    print()

    # Calc Student List and Print
    CalcStudentList(st_data_list)
    print("After CalcStudentList(st_data_list)")
    PrintStudentList(st_data_list)
    print()

    # Write to File
    FWriteData(output_file_name, st_data_list)

    # Calc Avg each class, Print
    each_class_avg_list = CalEachClass(st_data_list)
    print("Averege score of each class")
    for key, value in each_class_avg_list.items():
        print("{:10} = {:4.2f}".format(key, value))
